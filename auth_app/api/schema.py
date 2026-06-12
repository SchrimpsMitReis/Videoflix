from drf_spectacular.utils import extend_schema
from rest_framework import serializers

# Registration View
class RegistrationUserResponseSerializer(serializers.Serializer):
    """Describe the user fields returned after registration."""

    id = serializers.IntegerField()
    email = serializers.EmailField()


class RegistrationResponseSerializer(serializers.Serializer):
    """Describe the standard registration response."""

    user = RegistrationUserResponseSerializer()
    token = serializers.CharField()


class RegistrationDevResponseSerializer(serializers.Serializer):
    """Describe the development registration response including its action link."""

    user = RegistrationUserResponseSerializer()
    token = serializers.CharField()
    link = serializers.URLField()

# ActivationView

class ActivationResponseSerializer(serializers.Serializer):
    """Describe a successful account activation response."""

    message = serializers.CharField()

# LoginView

class LoginUserResponseSerializer(serializers.Serializer):
    """Describe the user summary returned after login."""

    id = serializers.IntegerField()
    username = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    """Describe a successful login response."""

    detail = serializers.CharField()
    user = LoginUserResponseSerializer()

# LogoutView

class LogoutResponseSerializer(serializers.Serializer):
    """Describe a successful logout response."""

    detail = serializers.CharField()


class LogoutErrorResponseSerializer(serializers.Serializer):
    """Describe an unsuccessful logout response."""

    error = serializers.CharField()

# CookieTokenRefreshView

class TokenRefreshResponseSerializer(serializers.Serializer):
    """Describe a successful access-token refresh response."""

    detail = serializers.CharField()
    access = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    """Describe a generic API error response."""

    detail = serializers.CharField()

# PasswordResetView


class PasswordResetResponseSerializer(serializers.Serializer):
    """Describe the standard password-reset request response."""

    detail = serializers.CharField()


class PasswordResetDevResponseSerializer(serializers.Serializer):
    """Describe the development password-reset response including its link."""

    detail = serializers.CharField()
    link = serializers.URLField()

# PasswordConfirmView:

class PasswordConfirmResponseSerializer(serializers.Serializer):
    """Describe a successful password change response."""

    detail = serializers.CharField()
