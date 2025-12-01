from apps.locations.models import Location
import requests


def import_location_from_api(location_name_or_id, user=None):
    """
    Fetch a Pokémon location from the PokeAPI and save it to the DB.
    Returns the PokemonAbility instance if successful, else None.
    """
    url = f"https://pokeapi.co/api/v2/location/{location_name_or_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch location {location_name_or_id}: {response.status_code}")
        return None

    data = response.json()
    print(f"API CALL MADE FOR LOCATION {location_name_or_id}")

    location_id = data.get("id")
    
    internal_location_name = data.get("name", "")

    areas_entries = data.get("areas", [])
    area_names = []
    for area_entry in areas_entries:
        area_names.append(area_entry.get("name"))

    game_indices_entries = data.get("game_indices", [])
    game_indices = ()
    for indice_entry in game_indices_entries:
        generation_name = indice_entry.get("generation", {}).get("name", "")
        game_indices = (generation_name, indice_entry.get("game_index"))

    location_names_entries = data.get("names", [])
    location_name = ""
    for location_entry in location_names_entries:
        if location_entry.get("language", {}).get("name") == "en":
            location_name = location_entry.get("name")
            break

    region_name = data.get("region", {}).get("name", "")

    location, _ = Location.objects.update_or_create(
        location_name=location_name,
        defaults={
            "location_id": location_id,
            "internal_location_name": internal_location_name,
            "areas": area_names,
            "game_indices": game_indices,
            "region_name": region_name,
        },
    )

    if user:
        location.allowed_users.add(user)

    return location
