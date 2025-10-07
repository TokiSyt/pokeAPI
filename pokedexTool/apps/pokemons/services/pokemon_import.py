import requests
from apps.pokemons.models import (
    Pokemon,
    PokemonType,
    PokemonTypeRelation,
    PokemonAbility,
    PokemonAbilityRelation,
    PokemonStat,
)
from django.db import transaction

'''
BULK CREATE FOR THE POKEDEX LIST
DISABLING THIS FUNCTION TO LIMIT API CALLS FOR THE POKE API SERVICE - USE AT YOUR OWN RISK

If you wish to use this, go to pokedexTool\apps\pokemons\management\commands\import_pokemon_list.py
uncomment the file, this function and type python manage.py import_pokemon_list at the root level

def pokemon_list_import_from_api(pokemon_index) -> Pokemon | None:
    """
    Fetch all pokemons basic information from the PokeAPI and save it to the DB.
    Returns the basic pokemons instances if successful, else None.
    """

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_index}")

    if response.status_code != 200:

        print(f"Failed to fetch Pokémon {pokemon_index}")
        return None

    data = response.json()
    print(f"API CALL MADE FOR POKEMON {data['name']}")

    return Pokemon(
            pokemon_id=data["id"],
            name=data["name"],
            sprite_front_default=data["sprites"]["front_default"],
        )


with ThreadPoolExecutor(max_workers=10) as executor:
    pokemons = list(executor.map(pokemon_list_import_from_api, range(1, 1025)))
    pokemons = [poke for poke in pokemons if poke is not None]

Pokemon.objects.bulk_create(pokemons, ignore_conflicts=True)
'''

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

    pokemon, _ = Pokemon.objects.update_or_create(
        pokemon_id=data["id"],
        defaults={
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "base_experience": data.get("base_experience"),
            "sprite_front_default": data["sprites"]["front_default"],
            "sprite_front_shiny": data["sprites"].get("front_shiny"),
        },
    )
    pokemon.allowed_users.add(user)

    for type_data in data["types"]:
        type_obj, _ = PokemonType.objects.get_or_create(name=type_data["type"]["name"])
        PokemonTypeRelation.objects.update_or_create(
            pokemon=pokemon, type=type_obj, slot=type_data["slot"]
        )

    for ability_data in data["abilities"]:
        ability_obj, _ = PokemonAbility.objects.get_or_create(
            name=ability_data["ability"]["name"]
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
