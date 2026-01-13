from django.urls import path

from .views import MovesSearchView

app_name = "berries"

urlpatterns = [
    path("", MovesSearchView.as_view(), name="berries-search"),
    path("<str:pokemon_type>", MovesSearchView.as_view(), name="berries-detail"),
]
