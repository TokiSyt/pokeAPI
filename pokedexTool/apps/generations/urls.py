from django.urls import path

from .views import GenDetailView, GenSearchView

app_name = "generations"

urlpatterns = [
    path("", GenSearchView.as_view(), name="gen-search"),
    path("<str:generation_name_or_id>", GenDetailView.as_view(), name="gen-detail"),
]
