from apps.pokemons.models import (
    Pokemon,
    PokemonType,
    PokemonTypeRelation,
    PokemonAbilityRelation,
    PokemonStat,
)

from apps.poke_types.services.import_type_from_api import import_pokemon_type_from_api
from apps.abilities.services.import_ability_from_api import (
    import_pokemon_ability_from_api,
)
from apps.abilities.models import PokemonAbility
from django.db import transaction
import requests


@transaction.atomic
def import_pokemon_from_api(pokemon_name: str, user) -> Pokemon | None:
    """
    Fetch a Pokemon from the PokeAPI and save it to the DB.
    Returns the Pokemon instance if successful, else None.
    """

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    if response.status_code != 200:
        return None

    data = response.json()
    print(f"API CALL MADE FOR POKEMON {pokemon_name}")

    if "moves" in data:
        move_names = [move["move"]["name"] for move in data.get("moves", [])]

    pokemon, _ = Pokemon.objects.update_or_create(
        pokemon_id=data["id"],
        defaults={
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "base_experience": data.get("base_experience"),
            "moves": move_names,
            "sprite_front_default": data["sprites"]["front_default"],
            "sprite_front_shiny": data["sprites"].get("front_shiny"),
        },
    )

    pokemon.allowed_users.add(user)

    for type_data in data["types"]:
        type_name = type_data["type"]["name"]
        type_obj_qs = PokemonType.objects.filter(name=type_name)

        if not type_obj_qs.exists():
            type_obj = import_pokemon_type_from_api(type_name)
        else:
            type_obj = PokemonType.objects.get(name=type_name)

        PokemonTypeRelation.objects.update_or_create(
            pokemon=pokemon, type=type_obj, slot=type_data["slot"]
        )

    for ability_data in data["abilities"]:

        ability_name = ability_data["ability"]["name"]
        ability_obj_qs = PokemonAbility.objects.filter(name=ability_name)

        if not ability_obj_qs.exists():
            ability_obj = import_pokemon_ability_from_api(ability_name)
        else:
            ability_obj = PokemonAbility.objects.get(name=ability_name)

        PokemonAbilityRelation.objects.update_or_create(
            pokemon=pokemon,
            ability=ability_obj,
            defaults={
                "is_hidden": ability_data["is_hidden"],
                "slot": ability_data["slot"],
            },
        )

    for stat_data in data["stats"]:
        PokemonStat.objects.update_or_create(
            pokemon=pokemon,
            stat_name=stat_data["stat"]["name"],
            defaults={
                "base_stat": stat_data["base_stat"],
                "effort": stat_data["effort"],
            },
        )

    return pokemon
