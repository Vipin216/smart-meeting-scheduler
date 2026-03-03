from rest_framework import viewsets, permissions
from .models import Meeting
from .serializers import MeetingSerializer


class MeetingViewSet(viewsets.ModelViewSet):

    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Meeting.objects.filter(host=self.request.user)

    def perform_destroy(self, instance):
        instance.status = 'Cancelled'
        instance.save()
