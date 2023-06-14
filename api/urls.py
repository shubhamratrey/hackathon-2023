from django.urls import include, re_path

from .home import urls as home_urls

urlpatterns = [
    re_path('^home/', include(home_urls)),
]
