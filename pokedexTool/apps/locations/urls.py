from .views import MovesSearchView
from django.urls import path

app_name = "locations"

urlpatterns = [
    path("", MovesSearchView.as_view(), name="locations-search"),
    path("<str:pokemon_type>", MovesSearchView.as_view(), name="locations-detail"),
]