from django.urls import path

from .views import MoveDetailView, MovesSearchView

app_name = "poke_moves"

urlpatterns = [
    path("", MovesSearchView.as_view(), name="moves-search"),
    path("<str:poke_move_name_or_id>", MoveDetailView.as_view(), name="move-detail"),
]
