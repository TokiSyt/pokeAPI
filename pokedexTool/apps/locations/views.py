from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import AreaSearchForm, LocationSearchForm
from .models import Area, Location
from .services.import_area_from_api import import_area_from_api
from .services.import_location_from_api import import_location_from_api


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


class LocationDetailView(LoginRequiredMixin, TemplateView):
    template_name = "locations/location_detail.html"

    def get(self, request, location_name_or_id):
        location_obj = None
        location_needs_update = False

        try:
            if location_name_or_id.isdigit():
                location_obj = Location.objects.get(Q(location_id=location_name_or_id))

            else:
                location_obj = Location.objects.get(
                    Q(internal_location_name=location_name_or_id)
                )

            if not location_obj.allowed_users.filter(id=self.request.user.id).exists():
                location_needs_update = True

            print(f"{location_obj.location_name} |")

            if not location_needs_update:
                print(f"location {location_obj.location_name} fetched from database")

        except Location.DoesNotExist:
            pass

        if location_needs_update or location_obj is None:
            location_obj = import_location_from_api(
                location_name_or_id, self.request.user
            )

        if not location_obj:
            context = {"error": f'Could not fetch location "{location_name_or_id}"'}

            return render(
                request,
                self.template_name,
                context,
                status=404,
            )

        else:
            context = {
                "location": location_obj,
            }

            return render(request, self.template_name, context)


class LocationAreaDetailView(LoginRequiredMixin, TemplateView):
    template_name = "locations/area_detail.html"

    def get(self, request, location_area_name_or_id):
        area_obj = None
        area_needs_update = False

        try:
            if location_area_name_or_id.isdigit():
                area_obj = Area.objects.get(Q(area_id=location_area_name_or_id))

            else:
                area_obj = Area.objects.get(
                    Q(internal_area_name=location_area_name_or_id)
                )

            if not area_obj.allowed_users.filter(id=self.request.user.id).exists():
                area_needs_update = True

            print(f"{area_obj.area_name} |")

            if not area_needs_update:
                print(f"area {area_obj.area_name} fetched from database")

        except Area.DoesNotExist:
            pass

        if area_needs_update or area_obj is None:
            area_obj = import_area_from_api(location_area_name_or_id, self.request.user)

        if not area_obj:
            context = {"error": f'Could not fetch area "{location_area_name_or_id}"'}

            return render(
                request,
                self.template_name,
                context,
                status=404,
            )

        else:
            context = {
                "area": area_obj,
            }

            return render(request, self.template_name, context)
