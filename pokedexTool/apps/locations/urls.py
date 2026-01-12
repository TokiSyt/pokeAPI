from django.urls import path

from .views import LocationAreaDetailView, LocationDetailView, LocationSearchView

app_name = "locations"

urlpatterns = [
    path("", LocationSearchView.as_view(), name="locations-search"),
    path(
        "<str:location_name_or_id>",
        LocationDetailView.as_view(),
        name="locations-detail",
    ),
    path(
        "area/<str:location_area_name_or_id>",
        LocationAreaDetailView.as_view(),
        name="locations-area-detail",
    ),
]
