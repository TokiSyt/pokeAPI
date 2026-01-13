from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Area, Location


class AreasListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Area
        fields = ["area_id", "area_name", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None

        return reverse(
            "api:api-area-detail",
            kwargs={"area_name": obj.area_name},
            request=request,
        )


class AreasDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            "encounter_method_rates",
            "area_id",
            "location",
            "internal_area_name",
            "area_name",
            "pokemon_encounters",
        ]


class LocationsListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Location
        fields = ["location_id", "location_name", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None

        return reverse(
            "api:api-location-detail",
            kwargs={"location_name": obj.location_name},
            request=request,
        )


class LocationsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "location_id",
            "internal_location_name",
            "location_name",
            "region_name",
            "areas",
            "game_indices",
        ]
