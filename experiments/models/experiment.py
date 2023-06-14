from django.db import models
from django.utils.text import slugify
import random
import string

from constants import (FLOW_STATUS)


class Video(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    youtube_url = models.CharField(max_length=512, null=False, db_index=True)
    input_language = models.CharField(max_length=512, null=False, db_index=True)
    output_language = models.CharField(max_length=512, null=False, db_index=True)
    status = models.CharField(max_length=100, null=False, default=FLOW_STATUS.IN_QUEUE)

    transcription = models.TextField(null=True)

    # is_active = models.BooleanField(default=True, db_index=True)
    # data = models.JSONField(default=dict)
    # original_media_url = models.CharField(max_length=512, default='', db_index=True)
    # hls_media_key = models.CharField(max_length=512, null=True, db_index=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_unique_slug(self):
        slug = slugify(self.title) + "-" + self.output_language
        while Video.objects.filter(slug=slug).exists():
            slug = slugify(self.title) + "-" + random.choice(list(string.ascii_uppercase))
        return slug
