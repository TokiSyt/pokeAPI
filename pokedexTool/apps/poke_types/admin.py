from django.contrib import admin

from .models import PokemonType, TypeDamageRelation

# Register your models here.

admin.site.register(PokemonType)
admin.site.register(TypeDamageRelation)
