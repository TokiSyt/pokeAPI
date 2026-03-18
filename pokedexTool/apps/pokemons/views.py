from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.views import PokeDetailView

from .forms import PokemonSearchForm
from .models import Pokemon, PokemonAbilityRelation, PokemonTypeRelation


class PokemonSearchView(LoginRequiredMixin, TemplateView):
    template_name = "pokemons/pokemon_search.html"
    form_class = PokemonSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        pokemons = Pokemon.objects.filter(allowed_users=self.request.user)
        context["pokemons"] = pokemons
        return context


class PokemonDetailView(PokeDetailView):
    model = Pokemon
    template_name = "pokemons/pokemon_detail.html"
    context_key = "pokemon"
    id_field = "pokemon_id"
    url_kwarg = "pokemon_name_or_id"
    error_noun = "Pokemon"

    def needs_reimport(self, obj, request):
        missing = (
            not obj.stats.exists()
            or not obj.type_relations.exists()
            or not obj.ability_relations.exists()
        )
        return missing or not obj.allowed_users.filter(id=request.user.id).exists()

    def build_context(self, obj, request):
        if len(obj.moves) < 3:
            obj.moves = []
        return {
            "pokemon": obj,
            "type_relations": PokemonTypeRelation.objects.filter(
                pokemon=obj
            ).select_related("type"),
            "ability_relations": PokemonAbilityRelation.objects.filter(
                pokemon=obj
            ).select_related("ability"),
            "stats": obj.stats.all(),
        }
