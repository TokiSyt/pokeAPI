from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    APIMenuView,
    PokemonListAPIView,
    PokemonDetailAPIView,
    PokemonMoveListAPIView,
    PokemonMoveDetailAPIView,
    PokemonAbilityListAPIView,
    PokemonAbilityDetailAPIView,
    PokemonTypeListAPIView,
    PokemonTypeDetailAPIView,
    LocationsAreasView,
    LocationsListAPIView,
    LocationDetailAPIView,
    AreasListAPIView,
    AreaDetailAPIView,
    GenerationsListAPIView,
    GenerationDetailAPIView
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
    path("types/", PokemonTypeListAPIView.as_view(), name="api-types-list"),
    path(
        "types/<str:pokemon_type_name>",
        PokemonTypeDetailAPIView.as_view(),
        name="api-type-detail",
    ),
    path("locations-areas", LocationsAreasView.as_view(), name="api-locations-areas"),
    path(
        "locations/",
        LocationsListAPIView.as_view(),
        name="api-locations-list",
    ),
    path(
        "locations/<str:location_name>",
        LocationDetailAPIView.as_view(),
        name="api-location-detail",
    ),
    path(
        "areas/",
        AreasListAPIView.as_view(),
        name="api-areas-list",
    ),
    path(
        "areas/<str:area_name>",
        AreaDetailAPIView.as_view(),
        name="api-area-detail",
    ),
    path("generations/", GenerationsListAPIView.as_view(), name="api-generations-list"),
    path(
        "generations/<str:generation_name>",
        GenerationDetailAPIView.as_view(),
        name="api-generation-detail",
    ),
]
