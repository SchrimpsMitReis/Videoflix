import django_rq

from auth_app.services.email_service import send_activation_link
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    if not instance.email:
        sender.objects.filter(pk=instance.pk).update(email=instance.username)
        instance.email = instance.username
    if instance.is_active and not instance.is_staff and not instance.is_superuser:
        sender.objects.filter(pk=instance.pk).update(is_active=False)
        instance.is_active = False
    print("Signal Gesendet", instance.email)
    queue = django_rq.get_queue("default")
    transaction.on_commit(
        lambda: queue.enqueue(send_activation_link, instance, job_timeout=60)
    )

