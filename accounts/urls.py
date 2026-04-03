from django.urls import path
from .google_login import google_login

urlpatterns = [
    path("google-login/", google_login),
]