from django.urls import include, re_path

from .lab import urls as home_urls

urlpatterns = [
    re_path('^lab/', include(home_urls)),
]
