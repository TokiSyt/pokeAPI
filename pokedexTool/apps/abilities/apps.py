from django.apps import AppConfig


class AbilitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.abilities"

    def ready(self):
        import apps.abilities.services.import_ability_from_api  # noqa: F401
