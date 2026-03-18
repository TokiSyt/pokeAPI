from django.apps import AppConfig


class GenerationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.generations"

    def ready(self):
        import apps.generations.services.import_generation_from_api  # noqa: F401
