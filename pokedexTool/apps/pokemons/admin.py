from django.contrib import admin
from .models import Pokemon,  PokemonTypeRelation, PokemonMoveRelation, PokemonAbilityRelation

# Register your models here.

admin.site.register(Pokemon)
admin.site.register(PokemonTypeRelation)
admin.site.register(PokemonMoveRelation)
admin.site.register(PokemonAbilityRelation)