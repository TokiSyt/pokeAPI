from django.db import transaction

from apps.core.import_service import register
from apps.core.pokeapi_client import default_client
from apps.poke_types.models import PokemonType, TypeDamageRelation


@register(PokemonType)
@transaction.atomic
def import_pokemon_type_from_api(name_or_id: str, user=None) -> PokemonType | None:
    """
    Fetch a Pokemon Type from the PokeAPI and save it to the DB.
    Returns the PokemonType instance if successful, else None.
    user param is accepted but unused — Type has no allowed_users field.
    """
    data = default_client.fetch("type", name_or_id)
    if data is None:
        return None

    gen_name = data.get("generation", {}).get("name", "")
    move_names = [move["name"] for move in data.get("moves", [])]

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
            "moves": move_names,
        },
    )

    relation, _ = TypeDamageRelation.objects.get_or_create(type=type_obj)
    damage_data = data.get("damage_relations", {})

    if damage_data:
        relation.double_damage_from = ",".join(
            [t["name"] for t in damage_data.get("double_damage_from", [])]
        )
        relation.half_damage_from = ",".join(
            [t["name"] for t in damage_data.get("half_damage_from", [])]
        )
        relation.no_damage_from = ",".join(
            [t["name"] for t in damage_data.get("no_damage_from", [])]
        )
        relation.double_damage_to = ",".join(
            [t["name"] for t in damage_data.get("double_damage_to", [])]
        )
        relation.half_damage_to = ",".join(
            [t["name"] for t in damage_data.get("half_damage_to", [])]
        )
        relation.no_damage_to = ",".join(
            [t["name"] for t in damage_data.get("no_damage_to", [])]
        )
        relation.save()

    return type_obj
