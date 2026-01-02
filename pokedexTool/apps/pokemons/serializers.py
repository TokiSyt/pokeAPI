from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import (
    Pokemon,
    PokemonTypeRelation,
    PokemonAbilityRelation,
    PokemonStat,
)


class PokemonSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pokemon
        fields = ["pokemon_id", "name", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None

        return reverse(
            "api:api-poke-detail",
            kwargs={"pokemon_name": obj.name},
            request=request,
        )


class PokemonTypeRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonTypeRelation
        fields = ["pokemon", "type", "slot"]


class PokemonAbilityRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonAbilityRelation
        fields = ["pokemon", "ability", "is_hidden", "slot"]


class PokemonStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonStat
        fields = ["pokemon", "stat_name", "base_stat", "effort"]


class PokemonDetailSerializer(serializers.ModelSerializer):
    type_relations = PokemonTypeRelationSerializer(many=True, read_only=True)
    ability_relations = PokemonAbilityRelationSerializer(many=True, read_only=True)
    stats = PokemonStatSerializer(many=True, read_only=True)
    moves = serializers.SerializerMethodField()

    class Meta:
        model = Pokemon
        fields = [
            "pokemon_id",
            "name",
            "height",
            "weight",
            "base_experience",
            "type_relations",
            "moves",
            "ability_relations",
            "stats",
        ]

    def get_moves(self, obj):
        moves_dict = {}
        moves = [
            move.replace("'", "").replace("[", "").replace("]", "").strip()
            for move in obj.moves.split(",")
        ]
        moves_dict["moves"] = moves

        return moves_dict
