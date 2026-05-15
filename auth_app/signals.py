import os
import django_rq

from auth_app.services.email_service import send_activation_link
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    instance.email = instance.username
    instance.is_active = False
    print("Signal Gesendet", instance.email)
    send_activation_link(instance)







# @receiver(post_delete, sender=Video)
# def user_delete_file_on_delete(sender, instance, **kwargs):
#     if instance.video_file and os.path.isfile(instance.video_file.path):
#         os.remove(instance.video_file.path)



