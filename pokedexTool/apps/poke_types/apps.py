from django.apps import AppConfig


class PokeTypesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.poke_types"

    def ready(self):
        import apps.poke_types.services.import_type_from_api  # noqa: F401
