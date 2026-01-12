import requests

from apps.moves.models import PokemonMove


def create_or_update_move(poke_move_name_or_id, user=None):
    """
    Fetch a Pokémon move from the PokeAPI and save it to the DB.
    """
    url = f"https://pokeapi.co/api/v2/move/{poke_move_name_or_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch move {poke_move_name_or_id}: {response.status_code}")
        return None

    data = response.json()
    print(f"API CALL MADE FOR MOVE {poke_move_name_or_id}")

    move_name = data.get("name")
    move_type = data.get("type", {}).get("name", "")

    damage_class = data.get("damage_class", {}).get("name", "")
    generation = data.get("generation", {}).get("name", "")
    category = (
        data.get("meta", {}).get("category", {}).get("name", "")
        if data.get("meta")
        else ""
    )

    ailment = (
        data.get("meta", {}).get("ailment", {}).get("name", "")
        if data.get("meta")
        else ""
    )
    ailment_chance = (
        data.get("meta", {}).get("ailment_chance", 0) if data.get("meta") else 0
    )

    effect_entries = data.get("effect_entries", [])
    effect = ""
    short_effect = ""
    for entry in effect_entries:
        if entry.get("language", {}).get("name") == "en":
            effect = entry.get("effect", "")
            short_effect = entry.get("short_effect", "")
            break

    flavor_text_entries = data.get("flavor_text_entries", [])
    flavor_text = ""
    for entry in flavor_text_entries:
        if entry.get("language", {}).get("name") == "en":
            flavor_text = entry.get("flavor_text", "")
            break

    ability, _ = PokemonMove.objects.update_or_create(
        name=move_name,
        defaults={
            "accuracy": data.get("accuracy"),
            "power": data.get("power"),
            "move_id": data.get("id"),
            "pp": data.get("pp"),
            "priority": data.get("priority"),
            "effect_chance": data.get("effect_chance"),
            "type": move_type,
            "damage_class": damage_class,
            "generation": generation,
            "category": category,
            "ailment": ailment,
            "ailment_chance": ailment_chance,
            "short_effect": short_effect,
            "effect": effect,
            "flavor_text": flavor_text,
        },
    )

    if user:
        ability.allowed_users.add(user)

    return ability
