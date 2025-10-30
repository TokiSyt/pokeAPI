from rest_framework.authtoken.views import obtain_auth_token
from .views import PokemonDetailAPIView, PokemonListAPIView
from django.urls import path

app_name = "api"

urlpatterns = [
    path("auth/", obtain_auth_token),
    path("pokemons/", PokemonListAPIView.as_view(), name="api-poke-list"),
    path("<str:pokemon_name>", PokemonDetailAPIView.as_view(), name="api-poke-detail"),
]
