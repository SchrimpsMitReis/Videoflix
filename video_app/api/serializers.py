from rest_framework import serializers

from video_app.models import Video



class VideoSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_thumbnail(self, obj):
        """
        The given Frontend allways trys to get the image with its domain so the request_url must be absolute!
        """
        request = self.context.get("request")

        if obj.thumbnail_url:
            return request.build_absolute_uri(obj.thumbnail_url)

        return None