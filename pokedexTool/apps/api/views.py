from apps.pokemons.serializers import PokemonSerializer
from .mixins import AdminUserPermissionMixin
from apps.pokemons.models import Pokemon
from rest_framework import generics

# Create your views here.

class PokemonDetailAPIView(AdminUserPermissionMixin, generics.RetrieveAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    lookup_field = "name"
    lookup_url_kwarg = "pokemon_name"
    
class PokemonListAPIView(generics.ListAPIView):

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    lookup_field = 'name'