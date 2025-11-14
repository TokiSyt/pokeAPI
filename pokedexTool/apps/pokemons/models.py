from django.conf import settings
from django.db import models
from apps.poke_types.models import PokemonType
from apps.moves.models import PokemonAbility

# Create your models here.


class Pokemon(models.Model):
    
    """
    Represents a Pokémon.
    """

    pokemon_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    height = models.IntegerField()
    weight = models.IntegerField()
    base_experience = models.IntegerField()

    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="pokemons"
    )

    sprite_front_default = models.ImageField(
        upload_to="pokemon_sprites/", null=True, blank=True
    )
    sprite_front_shiny = models.ImageField(
        upload_to="pokemon_sprites/", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pokemon_id"]

    def __str__(self):
        return f"{self.name}_({self.pokemon_id})"


class PokemonTypeRelation(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name="type_relations"
    )
    type = models.ForeignKey(PokemonType, on_delete=models.CASCADE)
    slot = models.IntegerField()

    class Meta:
        unique_together = ["pokemon", "type", "slot"]
        ordering = ["slot"]


class PokemonAbilityRelation(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name="ability_relations"
    )
    ability = models.ForeignKey(PokemonAbility, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)
    slot = models.IntegerField()

    class Meta:
        unique_together = ["pokemon", "ability", "slot"]
        ordering = ["slot", "is_hidden"]


class PokemonStat(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="stats")
    stat_name = models.CharField(max_length=50)  # hp, attack, defense, etc.
    base_stat = models.IntegerField()
    effort = models.IntegerField()

    class Meta:
        unique_together = ["pokemon", "stat_name"]
