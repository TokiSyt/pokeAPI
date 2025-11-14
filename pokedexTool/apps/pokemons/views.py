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
        type_relations = None
        moves_relations = None
        pokemon_needs_update = False

        try:
            pokemon = Pokemon.objects.get(name=pokemon_name)
            type_relations = PokemonTypeRelation.objects.filter(pokemon=pokemon).select_related('type')
            moves_relations = PokemonAbilityRelation.objects.filter(pokemon=pokemon).select_related('ability')
            
            # any information missing from the model and it's relations
            if (
                (not pokemon.stats.exists() or not type_relations or not moves_relations)
                or not pokemon.allowed_users.filter(id=request.user.id).exists()
            ):
                pokemon_needs_update = True
            print(f"{pokemon} fetched from database")

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
                "type_relations": type_relations,
                "ability_relations": moves_relations,
                "stats": pokemon.stats.all(),
            }

            return render(request, self.template_name, context)