from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from auth_app.services.email_service import send_activation_link, send_password_reset_link
from auth_app.api.serializers import ActivationSerializer, PasswordConfirmSerializer, PasswordResetSerializer, RegistrationSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auth_app.api.authentications import CookieJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from core.settings import DEV_MODE


class RegistrationView(APIView):
    """
    API endpoint for registering a new user.
    Accessible without authentication.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new user account using the RegistrationSerializer.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False

        activation_data = send_activation_link(user)

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
                "token": activation_data['token']
            },
            status=status.HTTP_201_CREATED)

class ActivationView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):

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
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

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

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="LAX"
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="LAX"
        )

        return response

class CookieTokenRefreshView(TokenRefreshView):
    """
    Refresh the access token using the refresh token stored in cookies.
    """

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
            secure=True,
            samesite="LAX"
        )
        return response

class LogoutView(APIView):
    """
    Logout endpoint that deletes authentication cookies
    and blacklists the refresh token.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = []

    def post(self, request):
        """
        Invalidate the refresh token and remove authentication cookies.
        """

        try:

            self._blacklist_refresh_token(request)
            return self._create_success_response()

        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    def _blacklist_refresh_token(self, request):
        """
        Add the refresh token to the blacklist so it can no longer be used.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        refresh_token_to_delete = RefreshToken(refresh_token)
        refresh_token_to_delete.blacklist()

    def _create_success_response(self):
        response = Response(
            {"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie(
            key="access_token",
            path="/")
        response.delete_cookie(
            key="refresh_token",
            path="/"
        )

        return response


class PasswordResetView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

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

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        
        print("PASSWORD RESET VIEW WIRD GETROFFEN")

        data = self._combine_url_credentials_to_request_data(request, uidb64, token)
        serializer = PasswordConfirmSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"detail": "Your Password has been successfully reset."},
            status=status.HTTP_200_OK
        )
    
    def _combine_url_credentials_to_request_data(self, request, uidb64, token):
        data = request.data
        data['uidb64'] = uidb64
        data['token'] = token
        return data
