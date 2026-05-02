
import os

from django.http import FileResponse, Http404
from rest_framework.decorators import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from video_app.api.serializers import VideoSerializer
from video_app.models import Video


class VideoListView(APIView):

    def get(self, request):
        queryset = Video.objects.all()
        serializer = VideoSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

# class VideoView(APIView):
#     queryset = Video.objects.all()
#     serializer = VideoSerializer
    
#     def get(self, request):

#         return Response({"Say": "Hallo"})

# class VideoViewSet(ReadOnlyModelViewSet):

#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer

#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)

    

class VideoStreamView(APIView):

    def get(self, request, movie_id, resolution):
        video = Video.objects.get(id=movie_id)

        base_path = video.video_file.path  # dein Originalvideo
        base, _ = os.path.splitext(base_path)
        # Beispiel: /media/video_1_480p_hls/video_1_480p.m3u8
        playlist_path = os.path.join(
            f"{base}_hls",
            f"{os.path.basename(base)}_{resolution}.m3u8"
        )
        print("BananaPath: ", playlist_path)
        # /app/media/video/257593_hls/257593_480p.m3u8
        if not os.path.exists(playlist_path):
            raise Http404("Video oder Manifest nicht gefunden")

        return FileResponse(
            open(playlist_path, "rb"),
            content_type="application/vnd.apple.mpegurl"
        )
    
class VideoStreamSegmentView(APIView):

    def get(self, request, movie_id, resolution, segment):
        video = Video.objects.get(id=movie_id)

        base_path = video.video_file.path
        base, _ = os.path.splitext(base_path)

        segment_path = os.path.join(
            f"{base}_hls",
            segment
        )

        print("BananaPath:", segment_path)

        if not os.path.exists(segment_path):
            raise Http404("Video oder Segment nicht gefunden")

        return FileResponse(
            open(segment_path, "rb"),
            content_type="video/mp2t"
        )    
