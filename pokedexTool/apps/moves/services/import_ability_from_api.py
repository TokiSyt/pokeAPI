from apps.moves.models import PokemonAbility


def get_name(data, key):
    return (data.get(key) or {}).get("name", "")

def create_or_update_ability(data):
    name = data["name"]

    damage_class = get_name(data, "damage_class")
    move_type = get_name(data, "type")
    generation = get_name(data, "generation")
    meta = data.get("meta") or {}
    category = get_name(meta, "category")
    ailment = get_name(meta, "ailment")
    ailment_chance = meta.get("ailment_chance")

    short_effect = ""
    effect = ""
    for e in data.get("effect_entries", []):
        if e.get("language", {}).get("name") == "en":
            effect = e.get("effect", "")
            short_effect = e.get("short_effect", "")
            break

    flavor_texts = [
        f["flavor_text"]
        for f in data.get("flavor_text_entries", [])
        if f.get("language", {}).get("name") == "en"
    ]
    flavor_text = flavor_texts[-1] if flavor_texts else ""

    ability, _ = PokemonAbility.objects.update_or_create(
        name=name,
        defaults={
            "accuracy": data.get("accuracy"),
            "power": data.get("power"),
            "pp": data.get("pp"),
            "priority": data.get("priority"),
            "effect_chance": data.get("effect_chance"),
            "damage_class": damage_class,
            "type": move_type,
            "generation": generation,
            "category": category,
            "ailment": ailment,
            "ailment_chance": ailment_chance,
            "short_effect": short_effect,
            "effect": effect,
            "flavor_text": flavor_text,
        },
    )

    return ability
