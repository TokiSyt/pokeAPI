from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    APIMenuView,
    PokemonListAPIView,
    PokemonDetailAPIView,
    PokemonMoveListAPIView,
    PokemonMoveDetailAPIView,
    PokemonAbilityListAPIView,
    PokemonAbilityDetailAPIView,
)
from django.urls import path

app_name = "api"

urlpatterns = [
    path("", APIMenuView.as_view(), name="api-menu"),
    path("auth/", obtain_auth_token),
    path("pokemons/", PokemonListAPIView.as_view(), name="api-poke-list"),
    path(
        "pokemons/<str:pokemon_name>",
        PokemonDetailAPIView.as_view(),
        name="api-poke-detail",
    ),
    path("moves/", PokemonMoveListAPIView.as_view(), name="api-move-list"),
    path(
        "moves/<str:pokemon_move_name>",
        PokemonMoveDetailAPIView.as_view(),
        name="api-move-detail",
    ),
    path("abilities/", PokemonAbilityListAPIView.as_view(), name="api-ability-list"),
    path(
        "abilities/<str:pokemon_ability_name>",
        PokemonAbilityDetailAPIView.as_view(),
        name="api-ability-detail",
    ),
]
