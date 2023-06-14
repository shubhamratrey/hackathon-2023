from django.urls import re_path, path, register_converter
from django.views.decorators.csrf import csrf_exempt
from utils.decorator import login_required

from . import (DoubtQueryV1)

urlpatterns = [
    re_path('^doubt-query/$', csrf_exempt(DoubtQueryV1.as_versioned_view())),
]
