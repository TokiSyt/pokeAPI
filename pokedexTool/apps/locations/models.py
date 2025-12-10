from django.conf import settings
from django.db import models
import ast


class Location(models.Model):

    areas = models.TextField(blank=True)
    game_indices = models.TextField(blank=True)
    location_id = models.IntegerField(unique=True)

    # english version of "names" not "name" field.
    internal_location_name = models.CharField()
    location_name = models.TextField()
    region_name = models.TextField(blank=True)

    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="locations"
    )
    
    class Meta:
        ordering = ["location_id"]

    @property
    def areas_list(self):
        try:
            return ast.literal_eval(self.areas)
        except:
            return []

    @property
    def game_indices_list(self):
        try:
            value = ast.literal_eval(self.game_indices)
            if isinstance(value, tuple):
                return [value]

            if isinstance(value, list):
                return [
                    tuple(x) if isinstance(x, (list, tuple)) else (x,) for x in value
                ]
        except:
            return []
        
    def __str__(self):
        return f"{self.internal_location_name}_{self.location_id}"


class Area(models.Model):
    
    encounter_method_rates = models.TextField(blank=True) 
    area_id = models.IntegerField(unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    internal_area_name = models.CharField(max_length=200)
    area_name = models.CharField(max_length=200)
    pokemon_encounters = models.TextField(blank=True)
    
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="areas"
    )
    
    class Meta:
        ordering = ["area_id"]
    
    @property
    def encounter_method_rates_list(self):
        try:
            value = ast.literal_eval(self.encounter_method_rates)
            if isinstance(value, tuple):
                return [value]

            if isinstance(value, list):
                return [
                    tuple(x) if isinstance(x, (list, tuple)) else (x,) for x in value
                ]
        except (ValueError, SyntaxError):
            return []

    @property
    def pokemon_encounters_list(self):
        try:
            value = ast.literal_eval(self.pokemon_encounters)
            if isinstance(value, list):
                return value
        except (ValueError, SyntaxError):
            return []