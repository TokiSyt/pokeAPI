from django.contrib import admin
from .models import Pokemon,  PokemonTypeRelation, PokemonAbilityRelation

# Register your models here.

admin.site.register(Pokemon)
admin.site.register(PokemonTypeRelation)
admin.site.register(PokemonAbilityRelation)