from .views import PokemonDetailView, PokemonSearchView
from django.urls import path

app_name = "pokemons"

urlpatterns = [
    path("", PokemonSearchView.as_view(), name="poke-search"),
    path("<str:pokemon_name_or_id>", PokemonDetailView.as_view(), name="poke-detail"),
]
