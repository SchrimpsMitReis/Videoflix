from django.db import models

CATEGORY_CHOICES = [
    ('Anime', 'Anime'),
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Horror', 'Horror'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Documentary', 'Documentary'),
    ('Animation', 'Animation'),
    ('Thriller', 'Thriller'),
    ('Romance', 'Romance'),
    ('Fantasy', 'Fantasy'),
]

class Video(models.Model):
    """Store video metadata, source files, thumbnails, and HLS resolutions."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    thumbnail_url = models.FileField(upload_to='thumbnails/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Drama')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_file = models.FileField(upload_to='video/', blank=False, null=False)
    resolutions = models.JSONField(default=list, blank=True)

    def __str__(self):
        """Return the video title for human-readable representations."""

        return self.title
