from django.db import models
from django.conf import settings
import ast

class PokemonAbility(models.Model):
    """
    Represents a Pokémon ability with localized names, effects, and flavor text.
    """
    
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="pokemon_ability"
    )

    name = models.CharField(max_length=100, unique=True)
    ability_id = models.IntegerField(unique=True)

    generation = models.CharField(max_length=50, blank=True, null=True)
    is_main_series = models.BooleanField(default=True)

    names = models.TextField(blank=True, null=True, help_text="List of localized names (dicts)")
    effect_entries = models.TextField(blank=True, null=True, help_text="Localized effects (dicts)")
    flavor_text_entries = models.TextField(blank=True, null=True, help_text="Localized flavor texts (dicts)")

    pokemons = models.TextField(blank=True, null=True, help_text="List of Pokémon names or IDs that can have this ability")

    def __str__(self):
        return f"{self.name}_({self.ability_id})"

    @property
    def names_list(self):
        try:
            return ast.literal_eval(self.names) if self.names else []
        except:
            return []

    @property
    def effects_list(self):
        try:
            return ast.literal_eval(self.effect_entries) if self.effect_entries else []
        except:
            return []

    @property
    def flavor_text_list(self):
        try:
            return ast.literal_eval(self.flavor_text_entries) if self.flavor_text_entries else []
        except:
            return []

    @property
    def pokemons_list(self):
        try:
            return ast.literal_eval(self.pokemon) if self.pokemon else []
        except:
            return []

    class Meta:
        ordering = ["ability_id"]
