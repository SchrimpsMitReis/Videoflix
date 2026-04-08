from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that supports tokens from
    the Authorization header or from the "access_token" cookie.
    """

    def authenticate(self, request):
        """
        Authenticate a request using a JWT.

        Priority:
        1. Authorization header
        2. access_token cookie

        Returns:
            (user, validated_token) if authentication succeeds,
            otherwise None.
        """
        header = self.get_header(request)
        raw_token = ""
        
        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token