from django.urls import re_path, path, register_converter
from django.views.decorators.csrf import csrf_exempt
from utils.decorator import login_required

from . import (UploadVideoV1, GetVideoDetailV1)

urlpatterns = [
    re_path('^upload-video/$', csrf_exempt(UploadVideoV1.as_versioned_view())),
    re_path('^(?P<video_id>\d+)/detail/$', GetVideoDetailV1.as_versioned_view()),
]
