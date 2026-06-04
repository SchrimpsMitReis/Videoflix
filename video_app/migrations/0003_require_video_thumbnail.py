# Generated manually to make thumbnail_url required without an interactive prompt.

from django.db import migrations, models


def fill_missing_thumbnails(apps, schema_editor):
    Video = apps.get_model("video_app", "Video")
    Video.objects.filter(thumbnail_url__isnull=True).update(
        thumbnail_url="thumbnails/default.jpg"
    )
    Video.objects.filter(thumbnail_url="").update(
        thumbnail_url="thumbnails/default.jpg"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("video_app", "0002_alter_video_description"),
    ]

    operations = [
        migrations.RunPython(fill_missing_thumbnails, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="video",
            name="thumbnail_url",
            field=models.FileField(upload_to="thumbnails/"),
        ),
    ]
