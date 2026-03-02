from django.db import models
from django.conf import settings

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_meetings'
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='meetings'
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    location = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title