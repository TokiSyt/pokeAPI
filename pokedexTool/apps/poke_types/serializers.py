from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import PokemonType, TypeDamageRelation


class TypeDamageRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDamageRelation
        fields = [
            "type",
            "no_damage_to",
            "half_damage_to",
            "double_damage_to",
            "no_damage_from",
            "half_damage_from",
            "double_damage_from",
        ]


class PokemonTypeSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PokemonType
        fields = ["type_id", "name", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None

        return reverse(
            "api:api-type-detail",
            kwargs={"pokemon_type_name": obj.name},
            request=request,
        )


class PokemonTypeDetailSerializer(serializers.ModelSerializer):

    damage_relations = TypeDamageRelationSerializer(read_only=True)
    moves = serializers.SerializerMethodField()

    class Meta:
        model = PokemonType
        fields = [
            "name",
            "type_id",
            "generation",
            "move_damage_class",
            "damage_relations",
            "moves",
        ]
        
    def get_moves(self, obj):
        moves_dict = {}
        moves = [
            move.replace("'", "").replace("[", "").replace("]", "").strip()
            for move in obj.moves.split(",")
        ]
        moves_dict = moves

        return moves_dict