from django.db import models
from django.conf import settings

class PokemonMove(models.Model):
    
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="pokemon_moves"
    )

    name = models.CharField(max_length=100, unique=True)
    move_id = models.IntegerField(unique=True, null=True)
    accuracy = models.IntegerField(null=True, blank=True)
    power = models.IntegerField(null=True, blank=True)
    pp = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    effect_chance = models.IntegerField(null=True, blank=True)

    damage_class = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    generation = models.CharField(max_length=50, blank=True)

    category = models.CharField(max_length=100, blank=True)
    ailment = models.CharField(max_length=100, blank=True)
    ailment_chance = models.IntegerField(null=True, blank=True)

    short_effect = models.TextField(blank=True)
    effect = models.TextField(blank=True)
    flavor_text = models.TextField(blank=True)
    
    class Meta:
        ordering = ["move_id"]

    def __str__(self):
        return f"{self.name}_{self.move_id}"
