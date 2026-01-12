from django.urls import path

from .views import pokedexHomeView

app_name = "pokedex"

urlpatterns = [path("", pokedexHomeView.as_view(), name="poke-home")]
