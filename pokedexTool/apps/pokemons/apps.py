from django.apps import AppConfig


class PokemonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pokemons"

    def ready(self):
        import apps.pokemons.services.pokemon_import  # noqa: F401
