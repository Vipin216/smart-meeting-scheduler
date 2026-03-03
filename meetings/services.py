from django.db.models import Q
from rest_framework.exceptions import ValidationError
from .models import Meeting


class MeetingService:

    @staticmethod
    def check_overlap(user, start_time, end_time):
        return Meeting.objects.filter(
            host=user,
            status='Scheduled'
        ).filter(
            Q(start_time__lt=end_time) &
            Q(end_time__gt=start_time)
        ).exists()

    @staticmethod
    def create_meeting(user, validated_data):

        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        if start_time >= end_time:
            raise ValidationError("End time must be after start time")

        if MeetingService.check_overlap(user, start_time, end_time):
            raise ValidationError("Meeting overlaps with an existing meeting")

        meeting = Meeting.objects.create(
            host=user,
            **validated_data
        )

        return meeting