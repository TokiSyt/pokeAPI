from django.db import transaction

from apps.core.import_service import import_for_model, register
from apps.core.pokeapi_client import default_client
from apps.locations.models import Area, Location


@register(Area)
@transaction.atomic
def import_area_from_api(name_or_id: str, user=None) -> Area | None:
    """
    Fetch a Pokemon location area from the PokeAPI and save it to the DB.
    Resolves the parent Location through the registry (transitive dependency).
    """
    data = default_client.fetch("location-area", name_or_id)
    if data is None:
        return None

    encounter_method_rates = []
    for entry in data.get("encounter_method_rates", []):
        method_name = entry.get("encounter_method", {}).get("name", "")
        rate = entry["version_details"][0].get("rate")
        encounter_method_rates.append((method_name, rate))

    location_internal_name = data.get("location", {}).get("name", "")
    location_qs = Location.objects.filter(internal_location_name=location_internal_name)
    if location_qs.exists():
        location_obj = location_qs.get()
    else:
        location_obj = import_for_model(Location, location_internal_name)

    area_name = ""
    for entry in data.get("names", []):
        if entry.get("language", {}).get("name", "") == "en":
            area_name = entry.get("name", "")

    pokemon_encounters = [
        entry.get("pokemon", {}).get("name", "")
        for entry in data.get("pokemon_encounters", [])
    ]

    area, _ = Area.objects.update_or_create(
        internal_area_name=data.get("name", ""),
        defaults={
            "encounter_method_rates": encounter_method_rates,
            "area_id": data.get("id"),
            "location": location_obj,
            "area_name": area_name,
            "pokemon_encounters": pokemon_encounters,
        },
    )

    if user:
        area.allowed_users.add(user)

    return area
