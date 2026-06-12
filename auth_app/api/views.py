from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from auth_app.services.email_service import generate_link, send_password_reset_link
from auth_app.api.serializers import ActivationSerializer, PasswordConfirmSerializer, PasswordResetSerializer, RegistrationSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from core.settings import DEV_MODE
from django.conf import settings
from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema
from .schema import (
    LogoutErrorResponseSerializer,
    LogoutResponseSerializer,
    PasswordConfirmResponseSerializer,
    RegistrationResponseSerializer,
    RegistrationDevResponseSerializer,
    ActivationResponseSerializer,
    LoginResponseSerializer,
    TokenRefreshResponseSerializer, 
    ErrorResponseSerializer,
    PasswordResetResponseSerializer, PasswordResetDevResponseSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiParameter


class RegistrationView(APIView):
    """
    API endpoint for registering a new user.
    Accessible without authentication.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        operation_id="01_auth_register",
        summary="Register user",
        request=RegistrationSerializer,
        responses={
            201: RegistrationDevResponseSerializer if DEV_MODE else RegistrationResponseSerializer,
        },
        description="Creates a new inactive user account and sends an activation link by email.",
        )

    def post(self, request):
        """
        Create a new user account using the RegistrationSerializer.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        activation_data = generate_link(user, "activate")

        if DEV_MODE:
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email
                    },
                    "token": activation_data['token'],
                    "link": activation_data['link']

                },
                status=status.HTTP_201_CREATED)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email
                },
            },
            status=status.HTTP_201_CREATED)

class ActivationView(APIView):

    """
    GETs a request from the frontend, with a b64 coded UserID an a token
    if Serializer is valid it sets the useraccount on is_active == true
    """

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        operation_id="02_auth_activate",
        summary="Activate user account",
        description="Activates a user account using the uidb64 and token from the activation link.",
        parameters=[
            OpenApiParameter(
                name="uidb64",
                type=str,
                location=OpenApiParameter.PATH,
                description="Base64 encoded user ID",
            ),
            OpenApiParameter(
                name="token",
                type=str,
                location=OpenApiParameter.PATH,
                description="Activation token",
            ),
        ],
        responses={
            200: ActivationResponseSerializer,
        },
    )

    def get(self, request, uidb64, token):
        """Activate the account identified by a valid signed URL."""

        data = {
            'uidb64': uidb64,
            'token': token
        }

        serializer = ActivationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.is_active = True
        user.save()

        return Response(
            {"message": "Account successfully activated."},
            status=status.HTTP_200_OK
        )

class LoginView(TokenObtainPairView):
    """Authenticate a user and store the generated JWTs in cookies."""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        operation_id="03_auth_login",
        summary="Login user",
        description=(
            "Authenticates a user and sets access_token and refresh_token "
            "as HttpOnly cookies."
        ),
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
        },)

    def post(self, request, *args, **kwargs):
        """Validate credentials and return a response containing JWT cookies."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        user = serializer.user

        response = Response({
            "detail": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
            }
        },
            status=status.HTTP_200_OK
        )

        response = self._set_cookies(
            response=response,
            access=access,
            refresh=refresh
        )
        get_token(request)
        return response
    
    def _set_cookies(self, response, access, refresh):
        """Attach access and refresh tokens as HTTP-only response cookies."""

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/"
        )
        return response

class CookieTokenRefreshView(TokenRefreshView):
    """
    Refresh the access token using the refresh token stored in cookies.
    """
    @extend_schema(
        tags=["Auth"],
        operation_id="04_auth_token_refresh",
        summary="Refresh access token (via cookie)",
        description=(
            "Generates a new access token using the refresh_token stored in cookies. "
            "Sets a new access_token cookie if successful."
        ),
        # No request body is required because the refresh token comes from a cookie.
        request=None,
        parameters=[
            OpenApiParameter(
                name="refresh_token",
                type=str,
                location=OpenApiParameter.COOKIE,
                description="JWT refresh token stored in HttpOnly cookie",
                required=True,
            )
        ],
        responses={
            200: TokenRefreshResponseSerializer,
            401: ErrorResponseSerializer,
        },
    )

    def post(self, request, *args, **kwargs):
        """
        Generate a new access token if the refresh token is valid.
        """

        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"detail": "Refresh Token invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = serializer.validated_data.get("access")

        response = Response({
            "detail": "Token refreshed",
            "access": access_token
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/"
        )
        return response

class LogoutView(APIView):
    """
    Logout endpoint that deletes authentication cookies
    and blacklists the refresh token.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=["Auth"],
        operation_id="05_auth_logout",
        summary="Logout user",
        description=(
            "Blacklists the refresh token from the refresh_token cookie "
            "and deletes access_token and refresh_token cookies."
        ),
        request=None,
        parameters=[
            OpenApiParameter(
                name="refresh_token",
                type=str,
                location=OpenApiParameter.COOKIE,
                required=False,
                description="JWT refresh token stored in HttpOnly cookie.",
            ),
            OpenApiParameter(
                name="access_token",
                type=str,
                location=OpenApiParameter.COOKIE,
                required=False,
                description="JWT access token stored in HttpOnly cookie.",
            ),
        ],
        responses={
            200: LogoutResponseSerializer,
            400: LogoutErrorResponseSerializer,
        },
    )

    def post(self, request):
        """
        Invalidate the refresh token and remove authentication cookies.
        """
        self._blacklist_refresh_token(request)
        return self._create_success_response()

    def _blacklist_refresh_token(self, request):
        """
        Add the refresh token to the blacklist so it can no longer be used.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return
        try:
            refresh_token_to_delete = RefreshToken(refresh_token)
            refresh_token_to_delete.blacklist()
        except TokenError:
            pass

    def _create_success_response(self):
        """Create a successful response that expires all authentication cookies."""

        response = Response(
            {"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie(
            key="access_token",
            path="/",
            samesite="Lax",
        )
        response.delete_cookie(
            key="refresh_token",
            path="/",
            samesite="Lax",
        )
        response.delete_cookie(
            key=settings.CSRF_COOKIE_NAME,
            path=settings.CSRF_COOKIE_PATH,
            domain=settings.CSRF_COOKIE_DOMAIN,
            samesite=settings.CSRF_COOKIE_SAMESITE,
        )

        return response

class PasswordResetView(APIView):
    """Accept password-reset requests and send the reset email."""

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema( 
        tags=["Auth"],
        operation_id="06_auth_password_reset",
        summary="Request password reset",
        description="Sends a password reset link to the user's email address.",
        request=PasswordResetSerializer,
        responses={
            200: PasswordResetDevResponseSerializer if DEV_MODE else PasswordResetResponseSerializer,
        },
    )

    def post(self, request):
        """
        Create a new user account using the RegistrationSerializer.
        """
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        activation_data = send_password_reset_link(user)

        if DEV_MODE:
            return Response(
                {
                    "detail": "An email has been sent to reset your password.",
                    "link": activation_data['link']
                },
                status=status.HTTP_200_OK)

        return Response(
            {
                "detail": "An email has been sent to reset your password."
            },
            status=status.HTTP_200_OK)

class PasswordConfirmView(APIView):
    """Validate a password-reset link and save the submitted password."""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        operation_id="07_auth_password_confirm",
        summary="Confirm password reset",
        description=(
            "Resets the user's password using uidb64 and token from the URL "
            "and the new password from the request body."
        ),
        parameters=[
            OpenApiParameter(
                name="uidb64",
                type=str,
                location=OpenApiParameter.PATH,
                description="Base64 encoded user ID",
            ),
            OpenApiParameter(
                name="token",
                type=str,
                location=OpenApiParameter.PATH,
                description="Password reset token",
            ),
        ],
        request=PasswordConfirmSerializer,
        responses={
            200: PasswordConfirmResponseSerializer,
        },
    )

    def post(self, request, uidb64, token):
        """Validate reset credentials and persist the new password."""
        
        data = self._combine_url_credentials_to_request_data(request, uidb64, token)
        serializer = PasswordConfirmSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"detail": "Your Password has been successfully reset."},
            status=status.HTTP_200_OK
        )
    
    def _combine_url_credentials_to_request_data(self, request, uidb64, token):
        """Merge reset credentials from the URL into the request data."""

        data = request.data
        data['uidb64'] = uidb64
        data['token'] = token
        return data
