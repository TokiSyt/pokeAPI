from django.apps import AppConfig


class MovesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.moves"

    def ready(self):
        import apps.moves.services.import_move_from_api  # noqa: F401
