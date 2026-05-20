from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def get_sender_email():
    if settings.DEFAULT_FROM_EMAIL and settings.DEFAULT_FROM_EMAIL != "noreply@videoflix.local":
        return settings.DEFAULT_FROM_EMAIL
    return settings.EMAIL_HOST_USER


def generate_link(user, path):
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    token_ok = default_token_generator.check_token(user, token)
    if token_ok:
        print("token ok", token)
        #d8obns-52339f86aa6212bd35201f2f0da34e46
        #d8obns-52339f86aa6212bd35201f2f0da34e46
        #http://127.0.0.1:5500/pages/auth/activate.html?uid=MTM&token=d8obns-52339f86aa6212bd35201f2f0da34e46
    link = f"{settings.FRONTEND_BASE_URL}/pages/auth/{path}.html?uid={uidb64}&token={token}"
    activation_data = {
        "link": link,
        "token": token
     }
    return activation_data

def send_activation_link(user):
    activation_data = generate_link(user, "activate")
    send_mail(
        subject="Aktiviere deinen Account",
        message=f"Klick auf den Link: {activation_data['link']}",
        from_email=get_sender_email(),
        recipient_list=[user.email],
        html_message=f"<h1>Aktiviere deinen Account</h1><a href='{activation_data['link']}'>Jetzt aktivieren</a>",
        fail_silently=False
    )
    print("Mail was Sandy",user, activation_data)
    return activation_data


def send_password_reset_link(user):
    activation_data = generate_link(user, "password_confirm")

    send_mail(
        subject="Passwort zurücksetzen",
        message=f"Klick auf den Link: {activation_data['link']}",
        from_email=get_sender_email(),
        recipient_list=[user.email],
        html_message=f"<h1>Passwort zurücksetzen</h1><a href='{activation_data['link']}'>Jetzt zurücksetzen</a>",
        fail_silently=False
    )
    return activation_data
