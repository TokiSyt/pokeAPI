from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import AbilitySearchForm
from .models import PokemonAbility
from .services.import_ability_from_api import import_pokemon_ability_from_api

# Create your views here.


class AbilitySearchView(LoginRequiredMixin, TemplateView):
    template_name = "abilities/abilities_search.html"
    form_class = AbilitySearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        abilities = PokemonAbility.objects.filter(allowed_users=self.request.user)
        context["abilities"] = abilities
        return context


class AbilityDetailView(LoginRequiredMixin, TemplateView):
    template_name = "abilities/ability_detail.html"

    def get(self, request, poke_ability_name_or_id):
        ability_obj = None
        ability_obj_needs_update = False

        try:
            if poke_ability_name_or_id.isdigit():
                ability_obj = PokemonAbility.objects.get(
                    Q(ability_id=poke_ability_name_or_id)
                )

            elif not poke_ability_name_or_id.isdigit():
                ability_obj = PokemonAbility.objects.get(
                    Q(name=poke_ability_name_or_id)
                )

            print(f"DB fetch: {ability_obj}")

            if not ability_obj_needs_update:
                print(f"ability {ability_obj.name} fetched from database")

        except PokemonAbility.DoesNotExist:
            ability_obj_needs_update = True

        if ability_obj_needs_update or ability_obj is None:
            ability_obj = import_pokemon_ability_from_api(
                poke_ability_name_or_id, self.request.user
            )

        if not ability_obj:
            context = {"error": f'Could not fetch ability "{poke_ability_name_or_id}"'}

            return render(
                request,
                self.template_name,
                context,
                status=404,
            )

        else:
            context = {
                "ability": ability_obj,
            }

            return render(request, self.template_name, context)
