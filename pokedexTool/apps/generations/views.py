from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.views import PokeDetailView

from .forms import GenerationSearchForm
from .models import Generation


class GenSearchView(LoginRequiredMixin, TemplateView):
    template_name = "generations/gen_search.html"
    form_class = GenerationSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        generations = Generation.objects.filter(allowed_users=self.request.user)
        context["gens"] = generations
        return context


class GenDetailView(PokeDetailView):
    model = Generation
    template_name = "generations/gen_detail.html"
    context_key = "generation"
    name_field = "internal_name"
    id_field = "gen_id"
    url_kwarg = "generation_name_or_id"
    error_noun = "generation"
