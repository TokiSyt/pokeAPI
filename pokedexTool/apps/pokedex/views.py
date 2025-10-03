from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class pokedexHomeView(TemplateView):
    template_name = "pokedex/pokedex-home.html"
    