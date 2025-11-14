from .views import MovesSearchView
from django.urls import path

app_name = "types"

urlpatterns = [
    path("", MovesSearchView.as_view(), name="moves-search"),
    path("<str:pokemon_type>", MovesSearchView.as_view(), name="moves-detail"),
]