from django.db import models
import ast


class PokemonType(models.Model):
    """
    Represents a Pokémon elemental type.
    """

    name = models.CharField(max_length=50, unique=True)
    type_id = models.IntegerField()

    generation = models.CharField(max_length=50, null=True)

    move_damage_class = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="The class of damage inflicted by this type (physical, special, etc.).",
    )

    moves = models.CharField(null=True)

    def __str__(self):
        return f"{self.name}_({self.type_id})"

    @property
    def moves_list(self):
        try:
            moves_list = ast.literal_eval(self.moves)
            if not moves_list:
                return [" "]
            return moves_list
        except:
            return []

    class Meta:
        ordering = ["type_id"]


class TypeDamageRelation(models.Model):
    """
    Represents the damage relations between types (e.g. Fire -> double_damage_to Grass).
    """

    type = models.OneToOneField(
        PokemonType, on_delete=models.CASCADE, related_name="damage_relations"
    )

    no_damage_to = models.TextField(blank=True)
    half_damage_to = models.TextField(blank=True)
    double_damage_to = models.TextField(blank=True)
    no_damage_from = models.TextField(blank=True)
    half_damage_from = models.TextField(blank=True)
    double_damage_from = models.TextField(blank=True)

    def __str__(self):
        return f"Damage relations for {self.type.name}"
