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

from apps.pokemons.models import Pokemon
from apps.moves.models import PokemonMove
from apps.abilities.models import PokemonAbility


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
