from django.urls import path

from .views import AbilityDetailView, AbilitySearchView

app_name = "abilities"

urlpatterns = [
    path("", AbilitySearchView.as_view(), name="ability-search"),
    path(
        "<str:poke_ability_name_or_id>",
        AbilityDetailView.as_view(),
        name="ability-detail",
    ),
]
