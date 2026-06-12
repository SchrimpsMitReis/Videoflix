from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def get_sender_email():
    """Return the configured sender address for outgoing application emails."""

    if settings.DEFAULT_FROM_EMAIL and settings.DEFAULT_FROM_EMAIL != "noreply@videoflix.local":
        return settings.DEFAULT_FROM_EMAIL
    return settings.EMAIL_HOST_USER


def generate_link(user, path):
    """Create a signed frontend action link for the given user."""

    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    link = f"{settings.FRONTEND_BASE_URL}/pages/auth/{path}.html?uid={uidb64}&token={token}"
    return {
        "link": link,
        "token": token,
    }


def render_action_email(user, activation_data, title, intro_text, button_text):
    """Render the shared HTML template for account-related emails."""

    return render_to_string(
        "email/videoflix_action_email.html",
        {
            "title": title,
            "user_name": user.get_full_name() or user.email or user.username,
            "intro_text": intro_text,
            "button_text": button_text,
            "action_url": activation_data["link"],
        },
    )


def send_action_email(user, subject, message, html_message):
    """Send a plain-text and HTML email to the given user."""

    send_mail(
        subject=subject,
        message=message,
        from_email=get_sender_email(),
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_activation_link(user):
    """Generate and send an account activation link."""

    activation_data = generate_link(user, "activate")
    html_message = render_action_email(
        user=user,
        activation_data=activation_data,
        title="Confirm your email",
        intro_text=(
            "Thank you for registering with Videoflix. To complete your registration "
            "and verify your email address, please click the link below:"
        ),
        button_text="Activate account",
    )
    send_action_email(
        user=user,
        subject="Confirm your email",
        message=f"Activate your Videoflix account: {activation_data['link']}",
        html_message=html_message,
    )
    return activation_data


def send_password_reset_link(user):
    """Generate and send a password reset link."""

    activation_data = generate_link(user, "confirm_password")
    html_message = render_action_email(
        user=user,
        activation_data=activation_data,
        title="Reset your password",
        intro_text=(
            "We received a request to reset your Videoflix password. To choose a new "
            "password, please click the link below:"
        ),
        button_text="Reset password",
    )
    send_action_email(
        user=user,
        subject="Reset your password",
        message=f"Reset your Videoflix password: {activation_data['link']}",
        html_message=html_message,
    )
    return activation_data
