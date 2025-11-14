from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.pokemons.models import PokemonType
from apps.poke_types.forms import TypeSearchForm


# Create your views here.

class MovesSearchView(LoginRequiredMixin, TemplateView):
    template_name = "pokemons/move_search.html"
    form_class = TypeSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        pokemons = PokemonType.objects.all()
        context["pokemon_moves"] = pokemons
        return context


class MovesAPIView(LoginRequiredMixin, TemplateView):
    pass
