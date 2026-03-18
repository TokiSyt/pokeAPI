from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.views import PokeDetailView

from .forms import AreaSearchForm, LocationSearchForm
from .models import Area, Location


class LocationSearchView(LoginRequiredMixin, TemplateView):
    template_name = "locations/location_search.html"
    form_class = LocationSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_a"] = self.form_class()
        context["form_b"] = AreaSearchForm
        locations = Location.objects.filter(allowed_users=self.request.user)
        areas = Area.objects.filter(allowed_users=self.request.user)
        context["locations"] = locations
        context["areas"] = areas
        return context


class LocationDetailView(PokeDetailView):
    model = Location
    template_name = "locations/location_detail.html"
    context_key = "location"
    name_field = "internal_location_name"
    id_field = "location_id"
    url_kwarg = "location_name_or_id"
    error_noun = "location"


class LocationAreaDetailView(PokeDetailView):
    model = Area
    template_name = "locations/area_detail.html"
    context_key = "area"
    name_field = "internal_area_name"
    id_field = "area_id"
    url_kwarg = "location_area_name_or_id"
    error_noun = "area"
