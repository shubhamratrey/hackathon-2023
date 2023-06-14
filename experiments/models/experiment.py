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

    translated_text = models.TextField(null=True)
    transcription = models.TextField(null=True)
    voice_id = models.CharField(max_length=15, null=True)

    media_key = models.CharField(max_length=512, null=True)
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

    def get_s3_link(self):
        if self.media_key:
            return 'https://kuku-hackathon.s3.ap-south-1.amazonaws.com/{}'.format(self.media_key)
        else:
            return None

    def to_json(self):
        doc = {
            'id': self.pk,
            'title': self.title,
            'slug': self.slug,
            'youtube_link': self.youtube_url,
            'status': self.status,
            's3_link': self.get_s3_link(),
            'translated_text': self.translated_text,
            'transcription': self.transcription,
            'voice_id': self.voice_id
        }
        return doc
