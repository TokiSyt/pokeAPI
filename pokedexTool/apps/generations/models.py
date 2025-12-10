from django.conf import settings
from django.db import models
import ast

class Generation(models.Model):

    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="pokemon_generations"
    )

    abilities = models.TextField(blank=True)
    moves = models.TextField(blank=True)
    gen_id = models.IntegerField(unique=True)
    main_region = models.CharField(max_length=200)
    internal_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    types = models.TextField(blank=True)

    class Meta:
        ordering = ["gen_id"]

    @property
    def abilities_list(self):
        try:
            abilities_list = ast.literal_eval(self.abilities)
            if not abilities_list:
                return ["No abilities"]
            return abilities_list
        except:
            return []

    @property
    def moves_list(self):
        try:
            moves_list = ast.literal_eval(self.moves)
            if not moves_list:
                return ["No moves"]
            return moves_list
        except:
            return []

    @property
    def types_list(self):
        try:
            types_list = ast.literal_eval(self.types)
            if not types_list:
                return ["No types"]
            return types_list
        except:
            return []
