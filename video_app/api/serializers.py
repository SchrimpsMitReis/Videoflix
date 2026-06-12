from rest_framework import serializers

from video_app.models import Video



class VideoSerializer(serializers.ModelSerializer):
    """Serialize video metadata with an absolute thumbnail URL."""

    thumbnail = serializers.SerializerMethodField()

    class Meta:
        """Expose all video model fields through the API."""

        model = Video
        fields = '__all__'

    def get_thumbnail(self, obj):
        """Return an absolute thumbnail URL for the frontend."""

        request = self.context.get("request")

        if obj.thumbnail_url:
            return request.build_absolute_uri(obj.thumbnail_url)

        return None
