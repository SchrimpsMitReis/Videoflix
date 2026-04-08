import os
import django_rq

from video_app.tasks import convert_to_hls
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save


resolutions = [144, 240, 360, 480, 720, 1080, 1440, 2160]


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    queue = django_rq.get_queue("default")
    queue.enqueue(convert_to_hls, instance.id, job_timeout=60*60)


@receiver(post_delete, sender=Video)
def video_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file and os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)



