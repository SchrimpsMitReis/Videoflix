from rest_framework import serializers


class VideoStreamNotFoundSerializer(serializers.Serializer):
    """Describe an error response for an unavailable video stream."""

    detail = serializers.CharField()
