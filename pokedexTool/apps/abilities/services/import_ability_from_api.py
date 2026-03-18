from django.db import transaction

from apps.abilities.models import PokemonAbility
from apps.core.import_service import register
from apps.core.pokeapi_client import default_client


@register(PokemonAbility)
@transaction.atomic
def import_ability(name_or_id: str, user=None) -> PokemonAbility | None:
    """
    Fetch a Pokemon ability from the PokeAPI and save it to the database.
    Returns the PokemonAbility instance if successful, else None.
    """
    data = default_client.fetch("ability", name_or_id)
    if data is None:
        return None

    gen_name = data.get("generation", {}).get("name")
    is_main_series = data.get("is_main_series", True)

    names_list = [
        entry
        for entry in data.get("names", [])
        if entry.get("language", {}).get("name") == "en"
    ]
    effect_entries_list = [
        entry
        for entry in data.get("effect_entries", [])
        if entry.get("language", {}).get("name") == "en"
    ]
    flavor_text_list = [
        entry
        for entry in data.get("flavor_text_entries", [])
        if entry.get("language", {}).get("name") == "en"
    ]
    pokemon_list = [p["pokemon"]["name"] for p in data.get("pokemon", [])]

    seen = set()
    unique_flavor_text = []

    for entry in flavor_text_list:
        text = entry["flavor_text"].replace("\n", " ").strip()
        if text not in seen:
            seen.add(text)
            unique_flavor_text.append(entry)

    ability_obj, _ = PokemonAbility.objects.update_or_create(
        ability_id=data["id"],
        defaults={
            "name": data["name"],
            "generation": gen_name,
            "is_main_series": is_main_series,
            "names": names_list,
            "effect_entries": effect_entries_list,
            "flavor_text_entries": unique_flavor_text,
            "pokemons": pokemon_list,
        },
    )

    if user:
        ability_obj.allowed_users.add(user)

    return ability_obj
