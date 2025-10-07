from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class pokedexHomeView(LoginRequiredMixin, TemplateView):
    template_name = "pokedex/pokedex-home.html"
    