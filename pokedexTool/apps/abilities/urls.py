from .views import AbilitySearchView
from django.urls import path

app_name = "abilities"

urlpatterns = [
    path("", AbilitySearchView.as_view(), name="ability-search"),
    path("<str:pokemon_ability>", AbilitySearchView.as_view(), name="ability-detail"),
]