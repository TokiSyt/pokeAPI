from .views import MovesSearchView
from django.urls import path

app_name = "berries"

urlpatterns = [
    path("", MovesSearchView.as_view(), name="berries-search"),
    path("<str:pokemon_type>", MovesSearchView.as_view(), name="berries-detail"),
]