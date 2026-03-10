from rest_framework import viewsets, permissions
from .models import Meeting
from .serializers import MeetingSerializer
from integrations.models import GoogleToken
from integrations.google_calendar import create_google_calendar_event


class MeetingViewSet(viewsets.ModelViewSet):

    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Meeting.objects.filter(host=self.request.user, status="Scheduled")

    def perform_create(self, serializer):

        meeting = serializer.save()

        try:
            google_token = GoogleToken.objects.get(user=self.request.user)

            create_google_calendar_event(
                google_token.access_token,
                meeting
            )

        except GoogleToken.DoesNotExist:
            pass

    def perform_destroy(self, instance):
        instance.status = 'Cancelled'
        instance.save()