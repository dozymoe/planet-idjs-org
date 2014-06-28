from django.db import models

# Create your models here.

class PostIndex(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    guid = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
    )
    author_name = models.CharField(max_length=32)
    author_url = models.URLField()
    local_url = models.URLField()
    local_desc_url = models.URLField()
    published = models.DateTimeField()
    title = models.CharField(max_length=64)
    url = models.URLField()

    class Meta:
        index_together = (('year', 'month'),)
