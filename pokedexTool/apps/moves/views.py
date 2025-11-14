from .services.import_ability_from_api import create_or_update_ability
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from .models import PokemonAbility
from .forms import MoveSearchForm
from django.db.models import Q


# Moves


class MovesSearchView(LoginRequiredMixin, TemplateView):
    template_name = "moves/move_search.html"
    form_class = MoveSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        moves = PokemonAbility.objects.filter(allowed_users=self.request.user)
        context["moves"] = moves
        return context


class MoveDetailView(LoginRequiredMixin, TemplateView):

    template_name = "moves/move_detail.html"

    def get(self, request, poke_move_name_or_id):

        move_obj = None
        move_needs_update = False

        try:
            if poke_move_name_or_id.isdigit():
                move_obj = PokemonAbility.objects.get(Q(move_id=poke_move_name_or_id))

            else:
                move_obj = PokemonAbility.objects.get(Q(name=poke_move_name_or_id))

            if not move_obj.allowed_users.filter(id=self.request.user.id).exists():
                move_needs_update = True

            print(f"{move_obj} | ")
            
            if not move_needs_update:    
                print(f"type {move_obj.name} fetched from database")

        except PokemonAbility.DoesNotExist:
            pass

        if move_needs_update or move_obj is None:
            move_obj = create_or_update_ability(poke_move_name_or_id, self.request.user)

        if not move_obj:
            context = {"error": f'Could not fetch type "{poke_move_name_or_id}"'}

            return render(
                request,
                self.template_name,
                context,
                status=404,
            )

        else:
            move_obj.allowed_users
            context = {
                "move": move_obj,
            }

            return render(request, self.template_name, context)
