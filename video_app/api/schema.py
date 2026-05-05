from rest_framework import serializers


class VideoStreamNotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField()