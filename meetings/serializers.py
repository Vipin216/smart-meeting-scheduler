from rest_framework import serializers
from .models import Meeting
from .services import MeetingService


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ('host', 'status', 'google_event_id', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        return MeetingService.create_meeting(user, validated_data)