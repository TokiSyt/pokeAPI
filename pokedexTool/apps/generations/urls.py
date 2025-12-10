from .views import GenSearchView, GenDetailView
from django.urls import path

app_name = "generations"

urlpatterns = [
    path("", GenSearchView.as_view(), name="gen-search"),
    path("<str:generation_name_or_id>", GenDetailView.as_view(), name="gen-detail"),
]
