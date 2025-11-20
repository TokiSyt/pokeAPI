from .services.pokemon_import import import_pokemon_from_api
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import PokemonSearchForm
from django.shortcuts import render
from .models import Pokemon, PokemonTypeRelation, PokemonAbilityRelation


# POKEMONS
class PokemonSearchView(LoginRequiredMixin, TemplateView):

    template_name = "pokemons/pokemon_search.html"
    form_class = PokemonSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        pokemons = Pokemon.objects.filter(allowed_users=self.request.user)
        context["pokemons"] = pokemons
        return context


class PokemonDetailView(LoginRequiredMixin, TemplateView):

    template_name = "pokemons/pokemon_detail.html"

    def get(self, request, pokemon_name):

        pokemon = None
        pokemon_needs_update = False

        try:
            pokemon = Pokemon.objects.get(name=pokemon_name)

            # any information missing from the model and it's relations

            missing_pokemon_information = (
                not pokemon.stats.exists()
                or not pokemon.type_relations.exists()
                or not pokemon.ability_relations.exists()
            )

            if (
                missing_pokemon_information
                or not pokemon.allowed_users.filter(id=request.user.id).exists()
            ):
                pokemon_needs_update = True

            print(f"{pokemon} fetched from database")

        except Pokemon.DoesNotExist:
            pokemon_needs_update = True

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

        type_relations = PokemonTypeRelation.objects.filter(
            pokemon=pokemon
        ).select_related("type")

        ability_relations = PokemonAbilityRelation.objects.filter(
            pokemon=pokemon
        ).select_related("ability")

        print(type_relations)
        context = {
            "pokemon": pokemon,
            "type_relations": type_relations,
            "ability_relations": ability_relations,
            "stats": pokemon.stats.all(),
        }

        return render(request, self.template_name, context)
