from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import PokemonMove


class PokemonMoveSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PokemonMove
        fields = ["move_id", "name", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None

        return reverse(
            "api:api-move-detail",
            kwargs={"pokemon_move_name": obj.name},
            request=request,
        )


class PokemonMoveDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokemonMove
        fields = [
            "name",
            "move_id",
            "accuracy",
            "power",
            "pp",
            "priority",
            "effect_chance",
            "damage_class",
            "type",
            "generation",
            "category",
            "ailment",
            "ailment_chance",
            "short_effect",
            "flavor_text",
        ]
