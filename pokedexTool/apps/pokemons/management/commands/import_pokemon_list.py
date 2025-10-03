'''
from django.core.management.base import BaseCommand
from apps.pokemons.services.pokemon_import import pokemon_list_import_from_api

class Command(BaseCommand):
    help = "Import all basic Pokemon info from PokeAPI into the databas"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting Pokemon list import..."))
        pokemon_list_import_from_api()
        self.stdout.write(self.style.SUCCESS("Pokemon list import finished!"))
'''