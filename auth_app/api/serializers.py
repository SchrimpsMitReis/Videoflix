from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    Ensures email uniqueness and password confirmation.
    """
    
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password']
        
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_confirmed_password(self, value):
        """
        Check if password and confirmed_password match.
        """
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        """
        Ensure the email address is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        """
        Create and store a new user with a hashed password.
        """
        pw = self.validated_data['password']

        account = User(
            username=self.validated_data['email'],
            email=self.validated_data['email'],
            is_active=False,
        )
        account.set_password(pw)
        account.save()
        return account

class ActivationSerializer(serializers.Serializer):
    
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    
    def validate(self, attrs):
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')

        try:
          user_id =  force_str(urlsafe_base64_decode(uidb64))
          user = User.objects.get(pk=user_id)
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid activation link."})        
        
        if not default_token_generator.check_token(user, token):
            print("Token not ok!!!", token)
            raise serializers.ValidationError({"detail": "Invalid or expired token."})
        
        attrs["user"] = user
        return attrs
    
class LoginSerializer(TokenObtainPairSerializer):
        
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]

    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Ungültige Email oder Password")
          
        if not user.check_password(password):
            print(password)
            raise serializers.ValidationError("Ungültige Email oder Password", status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            raise serializers.ValidationError("Account not Activated")
        
        attrs["username"] = user.username
        data = super().validate(attrs)
        
        return data
    
class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate(self, attrs):

        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError("Ungültige Email oder Password")

        attrs['user'] = user
        return attrs

class PasswordConfirmSerializer(serializers.Serializer):

    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        user = self._check_attrs(uidb64, token,new_password,confirm_password)
        attrs["user"] = self._save_user_and_password(user, new_password)
        return attrs
    
    def _convert_and_check_user_id(self,uidb64):
        try:
          user_id =  force_str(urlsafe_base64_decode(uidb64))
          user = User.objects.get(pk=user_id)
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid activation link."})
        return user

    def _save_user_and_password(self, user, new_password):
        user.set_password(new_password)
        user.save()
        return user

    def _check_token(self, user, token):
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Invalid or expired token."})

    def _check_password(self, new_password,confirm_password):
        if not new_password == confirm_password:
            raise serializers.ValidationError({"detail": "Password dont match"})

    def _check_attrs(self, uidb64, token,new_password,confirm_password):
        user = self._convert_and_check_user_id(uidb64)
        self._check_token(user,token)
        self._check_password(new_password,confirm_password)
        return user
