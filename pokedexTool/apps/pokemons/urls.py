from .views import PokemonAPIView, PokemonSearchView
from django.urls import path

app_name = "pokemons"

urlpatterns = [
    path("", PokemonSearchView.as_view(), name="poke-search"),
    path("<str:pokemon_name>", PokemonAPIView.as_view(), name="poke-detail"),
]
