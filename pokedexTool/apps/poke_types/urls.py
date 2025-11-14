from .views import TypeSearchView, TypeDetailView
from django.urls import path

app_name = "poke_types"

urlpatterns = [
    path("", TypeSearchView.as_view(), name="types-search"),
    path("<str:poke_type_name_or_id>", TypeDetailView.as_view(), name="types-detail"),
]