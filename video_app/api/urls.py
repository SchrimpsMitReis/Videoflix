from django.urls import path, include
from rest_framework.routers import DefaultRouter

from video_app.api.views import VideoViewSet


router = DefaultRouter()
router.register("video", VideoViewSet, basename="video_view")

urlpatterns = router.urls
