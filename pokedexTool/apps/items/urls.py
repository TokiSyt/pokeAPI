from django.urls import path

from .views import MovesSearchView

app_name = "items"

urlpatterns = [
    path("", MovesSearchView.as_view(), name="items-search"),
    path("<str:pokemon_type>", MovesSearchView.as_view(), name="items-detail"),
]
