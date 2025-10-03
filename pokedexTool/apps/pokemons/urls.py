from django.urls import path
from .views import PokemonAPIView, PokemonSearchView

app_name = "pokemons"

urlpatterns = [
    path("", PokemonSearchView.as_view(), name="poke-search"),
    path('api/<str:pokemon_name>', PokemonAPIView.as_view(), name='poke-api'),
]
