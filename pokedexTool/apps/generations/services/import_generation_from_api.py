from apps.generations.models import Generation
import requests


def import_generation_from_api(gen_name_or_id, user=None):
    """
    Fetch a Pokémon generation from the PokeAPI and save it to the DB.
    """
    url = f"https://pokeapi.co/api/v2/generation/{gen_name_or_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch generation {gen_name_or_id}: {response.status_code}")
        return None

    data = response.json()
    print(f"API CALL MADE FOR GENERATION {gen_name_or_id}")

    abilities_entries = data.get("abilities", [])
    abilities = []
    for ability_entry in abilities_entries:
        abilities.append(ability_entry.get("name", ""))

    moves_entries = data.get("moves", [])
    moves = []
    for move_entry in moves_entries:
        moves.append(move_entry.get("name", ""))

    types_entries = data.get("types", [])
    types = []
    for type_entry in types_entries:
        types.append(type_entry.get("name", ""))

    gen_id = data.get("id")

    internal_name = data.get("name", "")

    generation_names_entries = data.get("names", [])
    generation_name = ""
    for generation_entry in generation_names_entries:
        if generation_entry.get("language", {}).get("name") == "en":
            generation_name = generation_entry.get("name")
            break

    main_region_name = data.get("main_region", {}).get("name", "")

    generation, _ = Generation.objects.update_or_create(
        name=generation_name,
        defaults={
            "gen_id": gen_id,
            "internal_name": internal_name,
            "main_region": main_region_name,
            "abilities": abilities,
            "moves": moves,
            "types": types,
        },
    )

    if user:
        generation.allowed_users.add(user)

    return generation
