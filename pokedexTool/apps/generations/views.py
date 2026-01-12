from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import GenerationSearchForm
from .models import Generation
from .services.import_generation_from_api import import_generation_from_api


class GenSearchView(LoginRequiredMixin, TemplateView):
    template_name = "generations/gen_search.html"
    form_class = GenerationSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        generations = Generation.objects.filter(allowed_users=self.request.user)
        context["gens"] = generations
        return context


class GenDetailView(LoginRequiredMixin, TemplateView):
    template_name = "generations/gen_detail.html"

    def get(self, request, generation_name_or_id):
        generation_obj = None
        generation_needs_update = False

        try:
            if generation_name_or_id.isdigit():
                generation_obj = Generation.objects.get(Q(gen_id=generation_name_or_id))

            else:
                generation_obj = Generation.objects.get(
                    Q(internal_name=generation_name_or_id)
                )

            if not generation_obj.allowed_users.filter(
                id=self.request.user.id
            ).exists():
                generation_needs_update = True

            print(f"{generation_obj.name} |")

            if not generation_needs_update:
                print(f"generation {generation_obj.name} fetched from database")

        except Generation.DoesNotExist:
            pass

        if generation_needs_update or generation_obj is None:
            generation_obj = import_generation_from_api(
                generation_name_or_id, self.request.user
            )

        if not generation_obj:
            context = {"error": f'Could not fetch generation "{generation_name_or_id}"'}

            return render(
                request,
                self.template_name,
                context,
                status=404,
            )

        else:
            context = {
                "generation": generation_obj,
            }

            return render(request, self.template_name, context)
