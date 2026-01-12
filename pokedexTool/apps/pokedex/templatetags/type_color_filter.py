from django import template

from apps.pokedex.core.constants import POKEMON_TYPE_COLORS

register = template.Library()


@register.filter
def type_color(type_name):
    return POKEMON_TYPE_COLORS.get(type_name.lower(), "#c9be5fff")


@register.filter
def split(value, delimiter=","):
    """Splits a string by the given delimiter and trims whitespace."""
    if not value:
        return []
    return [v.strip() for v in value.split(delimiter) if v.strip()]
