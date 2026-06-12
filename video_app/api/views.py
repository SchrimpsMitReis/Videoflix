
import os
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializers import VideoSerializer
from .schema import VideoStreamNotFoundSerializer
from django.http import FileResponse, Http404
from rest_framework.decorators import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from video_app.api.serializers import VideoSerializer
from video_app.models import Video


class VideoListView(APIView):
    """Return all videos available in the catalog."""

    @extend_schema(
        tags=["Video"],
        operation_id="01_Video_List",
        summary="List videos",
        description="Returns a list of all available videos.",
        responses={
            200: VideoSerializer(many=True),
        },
    )

    def get(self, request):
        """Serialize and return the complete video list."""

        queryset = Video.objects.all()
        serializer = VideoSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    

class VideoStreamView(APIView):
    """Serve an HLS media playlist for a requested video resolution."""

    @extend_schema(
        tags=["Video"],
        summary="Get HLS playlist",
        description="Returns the HLS .m3u8 playlist for a video in the requested resolution.",
        parameters=[
            OpenApiParameter(
                name="movie_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the video.",
            ),
            OpenApiParameter(
                name="resolution",
                type=str,
                location=OpenApiParameter.PATH,
                description="Requested resolution, e.g. 480p, 720p or 1080p.",
            ),
        ],
        responses={
            (200, "application/vnd.apple.mpegurl"): OpenApiTypes.STR,
            404: VideoStreamNotFoundSerializer,
        },
    )

    def get(self, request, movie_id, resolution):
        """Resolve and return the closest available HLS playlist."""

        video = Video.objects.get(id=movie_id)
        resolution = _check_resolution_in_resolutions(video, resolution)
        base_path = video.video_file.path 
        base, _ = os.path.splitext(base_path)
        playlist_path = os.path.join(
            f"{base}_hls",
            f"{os.path.basename(base)}_{resolution}.m3u8"
        )
        

        if not os.path.exists(playlist_path):
            raise Http404("Video oder Manifest nicht gefunden")

        return FileResponse(
            open(playlist_path, "rb"),
            content_type="application/vnd.apple.mpegurl"
        )
    
    
class VideoStreamSegmentView(APIView):
    """Serve individual transport-stream segments used by HLS playback."""

    @extend_schema(
        tags=["Video"],
        summary="Get HLS segment",
        description="Returns a .ts HLS video segment.",
        parameters=[
            OpenApiParameter(
                name="movie_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the video.",
            ),
            OpenApiParameter(
                name="resolution",
                type=str,
                location=OpenApiParameter.PATH,
                description="Requested resolution, e.g. 480p, 720p or 1080p.",
            ),
            OpenApiParameter(
                name="segment",
                type=str,
                location=OpenApiParameter.PATH,
                description="Segment filename, e.g. video_480p_001.ts.",
            ),
        ],
        responses={
            (200, "video/mp2t"): OpenApiTypes.BINARY,
            404: VideoStreamNotFoundSerializer,
        },
    )

    def get(self, request, movie_id, resolution, segment):
        """Resolve and return a requested HLS segment file."""

        video = Video.objects.get(id=movie_id)

        base_path = video.video_file.path
        base, _ = os.path.splitext(base_path)

        segment_path = os.path.join(
            f"{base}_hls",
            segment
        )

        if not os.path.exists(segment_path):
            raise Http404("Video oder Segment nicht gefunden")

        return FileResponse(
            open(segment_path, "rb"),
            content_type="video/mp2t"
        )    


def _check_resolution_in_resolutions(video, resolution):
    """Select the highest available resolution up to the requested height."""

    try:
        requested_height = int(resolution.removesuffix("p"))
        available_heights = [int(height) for height in video.resolutions]
        print(available_heights)
    except (AttributeError, TypeError, ValueError):
        raise Http404("Ungültige oder nicht verfügbare Auflösung")

    valid_heights = [
        height for height in available_heights if height <= requested_height
    ]

    if not valid_heights:
        raise Http404("Keine passende Auflösung verfügbar")

    return f"{max(valid_heights)}p"
