from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Generation


class GenerationSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Generation
        fields = ["gen_id", "name", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None

        return reverse(
            "api:api-generation-detail",
            kwargs={"generation_name": obj.internal_name},
            request=request,
        )


class GenerationDetailSerializer(serializers.ModelSerializer):

    moves = serializers.SerializerMethodField()
    abilities = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()

    class Meta:
        model = Generation
        fields = [
            "abilities",
            "moves",
            "gen_id",
            "main_region",
            "internal_name",
            "name",
            "types",
        ]

    def get_moves(self, obj):
        moves_dict = {}
        moves = [
            move.replace("'", "").replace("[", "").replace("]", "").strip()
            for move in obj.moves.split(",")
        ]
        moves_dict = moves

        return moves_dict

    def get_abilities(self, obj):
        abilities_dict = {}
        abilities = [
            ability.replace("'", "").replace("[", "").replace("]", "").strip()
            for ability in obj.moves.split(",")
        ]
        abilities_dict = abilities

        return abilities_dict

    def get_types(self, obj):
        types_dict = {}
        types = [
            type.replace("'", "").replace("[", "").replace("]", "").strip()
            for type in obj.moves.split(",")
        ]
        types_dict = types

        return types_dict
