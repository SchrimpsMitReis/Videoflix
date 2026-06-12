from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Configure video records in the Django admin interface."""

    readonly_fields = ("resolutions",)

    def get_exclude(self, request, obj=None):
        """Hide generated resolution metadata while creating a video."""

        if obj is None:
            return ("resolutions",)

        return super().get_exclude(request, obj)
