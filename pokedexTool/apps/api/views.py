from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import generics

from apps.abilities.models import PokemonAbility
from apps.abilities.serializers import (
    PokemonAbilityDetailSerializer,
    PokemonAbilitySerializer,
)
from apps.generations.models import Generation
from apps.generations.serializers import (
    GenerationDetailSerializer,
    GenerationSerializer,
)
from apps.locations.models import Area, Location
from apps.locations.serializers import (
    AreasDetailSerializer,
    AreasListSerializer,
    LocationsDetailSerializer,
    LocationsListSerializer,
)
from apps.moves.models import PokemonMove
from apps.moves.serializers import PokemonMoveDetailSerializer, PokemonMoveSerializer
from apps.poke_types.models import PokemonType
from apps.poke_types.serializers import (
    PokemonTypeDetailSerializer,
    PokemonTypeSerializer,
)
from apps.pokemons.models import Pokemon
from apps.pokemons.serializers import PokemonDetailSerializer, PokemonSerializer

from .mixins import AdminUserPermissionMixin


class APIMenuView(LoginRequiredMixin, TemplateView):
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
