from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .services.pokemon_import import import_pokemon_from_api
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework.views import APIView
from .forms import PokemonSearchForm
from django.shortcuts import render
from .models import Pokemon


class PokemonSearchView(TemplateView, LoginRequiredMixin):
    template_name = "pokemons/pokemon_search.html"
    form_class = PokemonSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        pokemons = Pokemon.objects.filter(allowed_users=self.request.user)
        context["pokemons"] = pokemons
        return context


class PokemonAPIView(APIView, LoginRequiredMixin):
    """
    API endpoint that takes a Pokemon name and returns data from PokeAPI.
    """

    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "pokemons/pokemon_detail.html"

    def get(self, request, pokemon_name):

        pokemon = None
        pokemon_needs_update = False

        try:
            pokemon = Pokemon.objects.get(name=pokemon_name)

            if not pokemon.stats.exists():
                pokemon_needs_update = True

        except Pokemon.DoesNotExist:
            pass

        if pokemon_needs_update or pokemon is None:
            pokemon = import_pokemon_from_api(pokemon_name, request.user)

        if not pokemon:
            context = {"error": f'Could not fetch Pokemon "{pokemon_name}"'}

            return render(
                request,
                self.template_name,
                context,
                status=404,
            )

        else:
            context = {
                "pokemon": pokemon,
                "type_relations": pokemon.type_relations.select_related("type").all(),
                "abilities_relations": pokemon.ability_relations.select_related(
                    "ability"
                ).all(),
                "stats": pokemon.stats.all(),
            }

            return render(request, self.template_name, context)
