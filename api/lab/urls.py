from django.urls import re_path, path, register_converter
from django.views.decorators.csrf import csrf_exempt
from utils.decorator import login_required

from . import (UploadVideoV1, GetVideoDetailV1, GetVideoItemsV1)

urlpatterns = [
    re_path('^upload-video/$', csrf_exempt(UploadVideoV1.as_versioned_view())),
    re_path('^video-detail/$', GetVideoDetailV1.as_versioned_view()),
    re_path('^video-items/$', login_required(GetVideoItemsV1.as_versioned_view())),
]
