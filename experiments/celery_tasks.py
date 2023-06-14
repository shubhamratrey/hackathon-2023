from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def generate_tutor_sharable_banner(tutor_id):
    return "Generated"
