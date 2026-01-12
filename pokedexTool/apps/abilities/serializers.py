from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import PokemonAbility


class PokemonAbilitySerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PokemonAbility
        fields = ["ability_id", "name", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None

        return reverse(
            "api:api-ability-detail",
            kwargs={"pokemon_ability_name": obj.name},
            request=request,
        )


class PokemonAbilityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonAbility
        fields = [
            "name",
            "ability_id",
            "generation",
            "is_main_series",
            "names",
            "effect_entries",
            "flavor_text_entries",
            "pokemons",
        ]
