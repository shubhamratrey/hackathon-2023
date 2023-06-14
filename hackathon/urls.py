"""
URL configuration for hackathon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.lab, name='lab')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='lab')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.http import HttpResponse
from django.urls import include, re_path, path


def elb_ping(request):
    return HttpResponse("ok.")


urlpatterns = [
    re_path(r'^v(?P<_v>[0-9.]+)/', include('api.urls')),
    path('elb-ping/', elb_ping),
]
