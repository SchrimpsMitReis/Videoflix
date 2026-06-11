from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ("resolutions",)

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ("resolutions",)

        return super().get_exclude(request, obj)
