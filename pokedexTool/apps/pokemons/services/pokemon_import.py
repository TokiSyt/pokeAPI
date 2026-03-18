from django.db import transaction

from apps.abilities.models import PokemonAbility
from apps.core.import_service import import_for_model, register
from apps.core.pokeapi_client import default_client
from apps.poke_types.models import PokemonType
from apps.pokemons.models import (
    Pokemon,
    PokemonAbilityRelation,
    PokemonStat,
    PokemonTypeRelation,
)


@register(Pokemon)
@transaction.atomic
def import_pokemon_from_api(name_or_id: str, user=None) -> Pokemon | None:
    """
    Fetch a Pokemon from the PokeAPI and save it to the DB.
    Resolves Type and Ability transitive dependencies through the registry.
    """
    data = default_client.fetch("pokemon", name_or_id)
    if data is None:
        return None

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

    if user:
        pokemon.allowed_users.add(user)

    for type_data in data["types"]:
        type_name = type_data["type"]["name"]
        type_qs = PokemonType.objects.filter(name=type_name)
        type_obj = (
            type_qs.get()
            if type_qs.exists()
            else import_for_model(PokemonType, type_name)
        )

        PokemonTypeRelation.objects.update_or_create(
            pokemon=pokemon, type=type_obj, slot=type_data["slot"]
        )

    for ability_data in data["abilities"]:
        ability_name = ability_data["ability"]["name"]
        ability_qs = PokemonAbility.objects.filter(name=ability_name)
        ability_obj = (
            ability_qs.get()
            if ability_qs.exists()
            else import_for_model(PokemonAbility, ability_name)
        )

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
