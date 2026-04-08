
from rest_framework.viewsets import ReadOnlyModelViewSet

from video_app.api.serializers import VideoSerializer
from video_app.models import Video







class VideoViewSet(ReadOnlyModelViewSet):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)