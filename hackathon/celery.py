from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackathon.settings")

app = Celery('hackathon')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_routes = {}
app.conf.beat_schedule = {}
app.autodiscover_tasks()
