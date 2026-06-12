from django.apps import AppConfig


class VideoAppConfig(AppConfig):
    """Configure the video app and load its signal handlers."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_app'

    def ready(self):
        """Import signal handlers when Django initializes the app."""
        from . import signals
