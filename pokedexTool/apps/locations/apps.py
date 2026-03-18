from django.apps import AppConfig


class LocationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.locations"

    def ready(self):
        import apps.locations.services.import_area_from_api  # noqa: F401
        import apps.locations.services.import_location_from_api  # noqa: F401
