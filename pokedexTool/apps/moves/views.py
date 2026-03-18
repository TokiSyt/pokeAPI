from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.views import PokeDetailView
from apps.moves.models import PokemonMove

from .forms import MoveSearchForm


class MovesSearchView(LoginRequiredMixin, TemplateView):
    template_name = "moves/move_search.html"
    form_class = MoveSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        moves = PokemonMove.objects.filter(allowed_users=self.request.user)
        context["moves"] = moves
        return context


class MoveDetailView(PokeDetailView):
    model = PokemonMove
    template_name = "moves/move_detail.html"
    context_key = "move"
    id_field = "move_id"
    url_kwarg = "poke_move_name_or_id"
    error_noun = "move"
