from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .mixins import AdminUserPermissionMixin
from rest_framework import generics

from apps.pokemons.serializers import PokemonSerializer, PokemonDetailSerializer
from apps.moves.serializers import PokemonMoveSerializer, PokemonMoveDetailSerializer
from apps.abilities.serializers import (
    PokemonAbilitySerializer,
    PokemonAbilityDetailSerializer,
)
from apps.poke_types.serializers import (
    PokemonTypeSerializer,
    PokemonTypeDetailSerializer,
)
from apps.locations.serializers import (
    LocationsListSerializer,
    AreasListSerializer,
    LocationsDetailSerializer,
    AreasDetailSerializer,
)
from apps.generations.serializers import (
    GenerationSerializer,
    GenerationDetailSerializer,
)

from apps.poke_types.models import PokemonType
from apps.pokemons.models import Pokemon
from apps.moves.models import PokemonMove
from apps.abilities.models import PokemonAbility
from apps.locations.models import Location, Area
from apps.generations.models import Generation


class APIMenuView(TemplateView, LoginRequiredMixin):
    template_name = "api/api_menu.html"


class PokemonListAPIView(generics.ListAPIView):

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    lookup_field = "name"


class PokemonDetailAPIView(AdminUserPermissionMixin, generics.RetrieveAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonDetailSerializer
    lookup_field = "name"
    lookup_url_kwarg = "pokemon_name"


class PokemonMoveListAPIView(generics.ListAPIView):

    queryset = PokemonMove.objects.all()
    serializer_class = PokemonMoveSerializer
    lookup_field = "name"


class PokemonMoveDetailAPIView(AdminUserPermissionMixin, generics.RetrieveAPIView):
    queryset = PokemonMove.objects.all()
    serializer_class = PokemonMoveDetailSerializer
    lookup_field = "name"
    lookup_url_kwarg = "pokemon_move_name"


class PokemonAbilityListAPIView(generics.ListAPIView):

    queryset = PokemonAbility.objects.all()
    serializer_class = PokemonAbilitySerializer
    lookup_field = "name"


class PokemonAbilityDetailAPIView(AdminUserPermissionMixin, generics.RetrieveAPIView):
    queryset = PokemonAbility.objects.all()
    serializer_class = PokemonAbilityDetailSerializer
    lookup_field = "name"
    lookup_url_kwarg = "pokemon_ability_name"


class PokemonTypeListAPIView(generics.ListAPIView):

    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer
    lookup_field = "name"


class PokemonTypeDetailAPIView(AdminUserPermissionMixin, generics.RetrieveAPIView):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeDetailSerializer
    lookup_field = "name"
    lookup_url_kwarg = "pokemon_type_name"


class LocationsAreasView(TemplateView, LoginRequiredMixin):
    template_name = "api/locations_areas.html"


class LocationsListAPIView(generics.ListAPIView):

    queryset = Location.objects.all()
    serializer_class = LocationsListSerializer
    lookup_field = "location_name"


class LocationDetailAPIView(AdminUserPermissionMixin, generics.RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationsDetailSerializer
    lookup_field = "location_name"
    lookup_url_kwarg = "location_name"


class AreasListAPIView(generics.ListAPIView):

    queryset = Area.objects.all()
    serializer_class = AreasListSerializer
    lookup_field = "area_name"


class AreaDetailAPIView(AdminUserPermissionMixin, generics.RetrieveAPIView):
    queryset = Area.objects.all()
    serializer_class = AreasDetailSerializer
    lookup_field = "area_name"
    lookup_url_kwarg = "area_name"


class GenerationsListAPIView(generics.ListAPIView):

    queryset = Generation.objects.all()
    serializer_class = GenerationSerializer
    lookup_field = "internal_name"


class GenerationDetailAPIView(AdminUserPermissionMixin, generics.RetrieveAPIView):
    queryset = Generation.objects.all()
    serializer_class = GenerationDetailSerializer
    lookup_field = "internal_name"
    lookup_url_kwarg = "generation_name"
