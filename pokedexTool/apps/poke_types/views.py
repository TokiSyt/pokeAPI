from .services.import_type_from_api import import_pokemon_type_from_api
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import PokemonType, TypeDamageRelation
from django.shortcuts import render
from .forms import TypeSearchForm
from django.db.models import Q


class TypeSearchView(LoginRequiredMixin, TemplateView):

    template_name = "poke_types/type_search.html"
    form_class = TypeSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        types = PokemonType.objects.all()
        context["types"] = types
        return context


class TypeDetailView(LoginRequiredMixin, TemplateView):

    template_name = "poke_types/type_detail.html"

    def get(self, request, poke_type_name_or_id):

        type_obj = None
        type_relation = None
        type_needs_update = False

        try:
            if poke_type_name_or_id.isdigit():
                type_obj = PokemonType.objects.get(Q(type_id=poke_type_name_or_id))

            else:
                type_obj = PokemonType.objects.get(Q(name=poke_type_name_or_id))

            type_relation = TypeDamageRelation.objects.get(type=type_obj)

            print(f"{type_obj} | {type_relation}")

            if not type_obj.moves.exists():
                type_needs_update = True
            
            if not type_needs_update:    
                print(f"type {type_obj.name} fetched from database")

        except PokemonType.DoesNotExist:
            pass

        if type_needs_update or type_obj is None:
            type_obj = import_pokemon_type_from_api(poke_type_name_or_id)

        if not type_obj:
            context = {"error": f'Could not fetch type "{poke_type_name_or_id}"'}

            return render(
                request,
                self.template_name,
                context,
                status=404,
            )

        else:
            context = {
                "type": type_obj,
                "type_relation": type_relation,
            }

            return render(request, self.template_name, context)
