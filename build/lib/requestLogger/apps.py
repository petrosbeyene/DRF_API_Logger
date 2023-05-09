from django.apps import AppConfig


class RequestloggerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "requestLogger"

    def ready(self) -> None:
        import requestLogger.signals
