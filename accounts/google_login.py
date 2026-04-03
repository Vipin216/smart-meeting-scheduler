from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import User


@api_view(["POST"])
def google_login(request):

    token = request.data.get("token")

    if not token:
        return Response({"error": "Token missing"}, status=400)

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except Exception:
        return Response({"error": "Invalid token"}, status=400)

    email = idinfo.get("email")
    name = idinfo.get("name", "")

    user, created = User.objects.get_or_create(
        email=email,
        defaults={"full_name": name}
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })