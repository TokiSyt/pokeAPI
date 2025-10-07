from rest_framework import serializers
from .models import Pokemon, PokemonType, PokemonAbility, PokemonStat


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ["pokemon_id", "name", "sprite_front_default"]


class PokemonDetailSerializer(serializers.ModelSerializer):
    type_relations = serializers.StringRelatedField(many=True)
    ability_realations = serializers.StringRelatedField(many=True)
    stats = serializers.StringRelatedField(many=True)

    class Meta:
        model = Pokemon
        fields = [
            "pokemon_id",
            "name",
            "height",
            "weight",
            "base_experience",
            "sprite_front_default",
            "sprite_front_shiny",
            "type_relations",
            "ability_relations",
            "stats",
        ]
