from django.urls import path, include
from rest_framework.routers import DefaultRouter

from video_app.api.views import VideoListView, VideoStreamSegmentView, VideoStreamView


# router = DefaultRouter()
# router.register("video", VideoViewSet, basename="video_view")

# urlpatterns = router.urls


urlpatterns = [
    path('video/', VideoListView.as_view(), name="video_list"),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoStreamView.as_view(), name="video_resolution"),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', VideoStreamSegmentView.as_view(), name="video_segment"),
]