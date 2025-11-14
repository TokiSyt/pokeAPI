from apps.moves.services.import_ability_from_api import create_or_update_ability
from apps.poke_types.models import PokemonType, TypeDamageRelation
from asgiref.sync import async_to_sync
from django.db import transaction
import requests
import asyncio
import aiohttp

@transaction.atomic
def import_pokemon_type_from_api(type_name_or_id: str) -> PokemonType | None:
    """
    Fetch a Pokémon Type from the PokeAPI and save it to the DB.
    Returns the Pokémon Type instance if successful, else None.
    """

    response = requests.get(f"https://pokeapi.co/api/v2/type/{type_name_or_id}")
    if response.status_code != 200:
        print(f"Failed to fetch type {type_name_or_id}: {response.status_code}")
        return None

    data = response.json()
    print(f"API CALL MADE FOR TYPE {type_name_or_id}")

    if "generation" in data and data["generation"]:
        gen_name = data["generation"]["name"]

    type_obj, _ = PokemonType.objects.update_or_create(
        name=data["name"],
        defaults={
            "type_id": data["id"],
            "generation": gen_name,
            "move_damage_class": (
                data.get("move_damage_class", {}).get("name")
                if data.get("move_damage_class")
                else None
            ),
        },
    )
    
    relation, _ = TypeDamageRelation.objects.get_or_create(type=type_obj)
    damage_data = data.get("damage_relations", {})
    
    if damage_data:
        
        relation.double_damage_from = ",".join([t["name"] for t in damage_data.get("double_damage_from", [])])
        relation.half_damage_from = ",".join([t["name"] for t in damage_data.get("half_damage_from", [])])
        relation.no_damage_from = ",".join([t["name"] for t in damage_data.get("no_damage_from", [])])
        relation.double_damage_to = ",".join([t["name"] for t in damage_data.get("double_damage_to", [])])
        relation.half_damage_to = ",".join([t["name"] for t in damage_data.get("half_damage_to", [])])
        relation.no_damage_to = ",".join([t["name"] for t in damage_data.get("no_damage_to", [])])

        relation.save()
        
    if "moves" in data:
        move_urls = [move["url"] for move in data["moves"]]
        moves_data = async_to_sync(fetch_all_moves)(move_urls)
        
        moves_list = []
        for move_data in moves_data:
            ability = create_or_update_ability(move_data)
            moves_list.append(ability)

        type_obj.moves.set(moves_list)
            

    return type_obj

async def fetch_move(session, url):
    async with session.get(url) as resp:
        return await resp.json()

async def fetch_all_moves(move_urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(fetch_move(session, url) for url in move_urls))
