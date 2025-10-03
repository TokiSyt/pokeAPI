from django import template
from apps.pokedex.core.constants import POKEMON_TYPE_COLORS

register = template.Library()

@register.filter
def type_color(type_name):
    return POKEMON_TYPE_COLORS.get(type_name.lower(), "#A8A77A")