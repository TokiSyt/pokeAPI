from django.db import transaction

from apps.core.import_service import register
from apps.core.pokeapi_client import default_client
from apps.locations.models import Location


@register(Location)
@transaction.atomic
def import_location_from_api(name_or_id: str, user=None) -> Location | None:
    """
    Fetch a Pokemon location from the PokeAPI and save it to the DB.
    """
    data = default_client.fetch("location", name_or_id)
    if data is None:
        return None

    area_names = [entry.get("name") for entry in data.get("areas", [])]

    game_indices: tuple = ()
    for entry in data.get("game_indices", []):
        game_indices = (
            entry.get("generation", {}).get("name", ""),
            entry.get("game_index"),
        )

    location_name = ""
    for entry in data.get("names", []):
        if entry.get("language", {}).get("name") == "en":
            location_name = entry.get("name")
            break

    location, _ = Location.objects.update_or_create(
        location_name=location_name,
        defaults={
            "location_id": data.get("id"),
            "internal_location_name": data.get("name", ""),
            "areas": area_names,
            "game_indices": game_indices,
            "region_name": data.get("region", {}).get("name", ""),
        },
    )

    if user:
        location.allowed_users.add(user)

    return location
