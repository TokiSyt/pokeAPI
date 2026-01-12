from django.contrib import admin

from .models import Pokemon, PokemonAbilityRelation, PokemonStat, PokemonTypeRelation

# Register your models here.

admin.site.register(Pokemon)
admin.site.register(PokemonTypeRelation)
admin.site.register(PokemonAbilityRelation)
admin.site.register(PokemonStat)
