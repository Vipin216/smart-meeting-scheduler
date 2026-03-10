import requests
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from .models import GoogleToken


def google_connect(request):

    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=https://www.googleapis.com/auth/calendar"
        "&access_type=offline"
        "&prompt=consent"
        f"&state={request.user.id}"
    )

    return HttpResponseRedirect(auth_url)


def google_callback(request):

    code = request.GET.get("code")
    user_id = request.GET.get("state")

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")

    expires_at = timezone.now() + timedelta(seconds=expires_in)

    user = User.objects.get(id=user_id)

    GoogleToken.objects.update_or_create(
        user=user,
        defaults={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
        }
    )

    return JsonResponse({"message": "Google account connected successfully"})