from apps.locations.models import Area, Location
from apps.locations.services.import_location_from_api import import_location_from_api
import requests


def import_area_from_api(location_area_name_or_id, user=None):
    """
    Fetch a Pokémon area from the PokeAPI and save it to the DB.
    """
    url = f"https://pokeapi.co/api/v2/location-area/{location_area_name_or_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f"Failed to fetch area {location_area_name_or_id}: {response.status_code}"
        )
        return None

    data = response.json()
    print(f"API CALL MADE FOR AREA {location_area_name_or_id}")

    encounter_method_rates_entries = data.get("encounter_method_rates", {})
    encounter_method_rates = []
    for encounter_rates_entry in encounter_method_rates_entries:
        encounter_method_name = encounter_rates_entry.get("encounter_method", {}).get(
            "name", ""
        )
        encounter_method_rate = encounter_rates_entry["version_details"][0].get(
            "rate"
        )
        encounter_method_rates.append((encounter_method_name, encounter_method_rate))
        

    area_id = data.get("id")
    location_name_entry = data.get("location", {}).get("name", "")
    location_obj_qs = Location.objects.filter(
        internal_location_name=location_name_entry
    )

    if not location_obj_qs.exists():
        location_obj = import_location_from_api(location_name_entry)
    else:
        location_obj = Location.objects.get(internal_location_name=location_name_entry)

    internal_area_name = data.get("name", "")

    area_name = ""
    area_name_entries = data.get("names", {})
    for area_name_entry in area_name_entries:
        if area_name_entry.get("language", {}).get("name", "") == "en":
            area_name = area_name_entry.get("name", "")

    pokemon_encounters_entries = data.get("pokemon_encounters", {})
    pokemon_encounters = []

    for pokemon_encounter_entry in pokemon_encounters_entries:
        pokemon_encounters.append(
            pokemon_encounter_entry.get("pokemon", {}).get("name", "")
        )

    area, _ = Area.objects.update_or_create(
        internal_area_name=internal_area_name,
        defaults={
            "encounter_method_rates": encounter_method_rates,
            "area_id": area_id,
            "location": location_obj,
            "internal_area_name": internal_area_name,
            "area_name": area_name,
            "pokemon_encounters": pokemon_encounters,
        },
    )

    if user:
        area.allowed_users.add(user)

    return area

