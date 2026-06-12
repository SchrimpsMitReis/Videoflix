from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Configure the authentication app and load its signal handlers."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        """Import signal handlers when Django initializes the app."""
        import auth_app.signals
