from django.db import transaction

from apps.core.import_service import register
from apps.core.pokeapi_client import default_client
from apps.generations.models import Generation


@register(Generation)
@transaction.atomic
def import_generation(name_or_id: str, user=None) -> Generation | None:
    """
    Fetch a Pokemon generation from the PokeAPI and save it to the DB.
    """
    data = default_client.fetch("generation", name_or_id)
    if data is None:
        return None

    abilities = [a.get("name", "") for a in data.get("abilities", [])]
    moves = [m.get("name", "") for m in data.get("moves", [])]
    types = [t.get("name", "") for t in data.get("types", [])]

    generation_name = ""
    for entry in data.get("names", []):
        if entry.get("language", {}).get("name") == "en":
            generation_name = entry.get("name")
            break

    main_region_name = data.get("main_region", {}).get("name", "")

    generation, _ = Generation.objects.update_or_create(
        name=generation_name,
        defaults={
            "gen_id": data.get("id"),
            "internal_name": data.get("name", ""),
            "main_region": main_region_name,
            "abilities": abilities,
            "moves": moves,
            "types": types,
        },
    )

    if user:
        generation.allowed_users.add(user)

    return generation
