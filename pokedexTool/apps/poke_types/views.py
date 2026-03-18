from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.views import PokeDetailView

from .forms import TypeSearchForm
from .models import PokemonType, TypeDamageRelation


class TypeSearchView(LoginRequiredMixin, TemplateView):
    template_name = "poke_types/type_search.html"
    form_class = TypeSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        types = PokemonType.objects.all()
        context["types"] = types
        return context


class TypeDetailView(PokeDetailView):
    model = PokemonType
    template_name = "poke_types/type_detail.html"
    context_key = "type"
    id_field = "type_id"
    url_kwarg = "poke_type_name_or_id"
    error_noun = "type"
    check_user = False

    def build_context(self, obj, request):
        return {
            "type": obj,
            "type_relation": TypeDamageRelation.objects.get(type=obj),
        }
