from django.urls import path, include

from auth_app.api.views import ActivationView, CookieTokenRefreshView, LoginView, LogoutView, PasswordConfirmView, PasswordResetView, RegistrationView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('activate/<str:uidb64>/<str:token>/', ActivationView.as_view(), name='activation'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_confirm/<str:uidb64>/<str:token>/', PasswordConfirmView.as_view(), name='password_confirm'),
]
