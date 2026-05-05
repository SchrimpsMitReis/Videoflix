from drf_spectacular.utils import extend_schema
from rest_framework import serializers

# Registration View
class RegistrationUserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()


class RegistrationResponseSerializer(serializers.Serializer):
    user = RegistrationUserResponseSerializer()
    token = serializers.CharField()


class RegistrationDevResponseSerializer(serializers.Serializer):
    user = RegistrationUserResponseSerializer()
    token = serializers.CharField()
    link = serializers.URLField()

# ActivationView

class ActivationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

# LoginView

class LoginUserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    user = LoginUserResponseSerializer()

# LogoutView

class LogoutResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class LogoutErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

# CookieTokenRefreshView

class TokenRefreshResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    access = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()

# PasswordResetView


class PasswordResetResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class PasswordResetDevResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    link = serializers.URLField()

# PasswordConfirmView:

class PasswordConfirmResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()