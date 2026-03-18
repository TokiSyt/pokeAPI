from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.views import PokeDetailView

from .forms import AbilitySearchForm
from .models import PokemonAbility


class AbilitySearchView(LoginRequiredMixin, TemplateView):
    template_name = "abilities/abilities_search.html"
    form_class = AbilitySearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        abilities = PokemonAbility.objects.filter(allowed_users=self.request.user)
        context["abilities"] = abilities
        return context


class AbilityDetailView(PokeDetailView):
    model = PokemonAbility
    template_name = "abilities/ability_detail.html"
    context_key = "ability"
    id_field = "ability_id"
    url_kwarg = "poke_ability_name_or_id"
    error_noun = "ability"
