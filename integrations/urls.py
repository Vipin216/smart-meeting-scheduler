from django.urls import path
from .google_views import google_connect, google_callback

urlpatterns = [
    path("connect/", google_connect),
    path("callback/", google_callback),
]