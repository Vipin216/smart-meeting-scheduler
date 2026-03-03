from django.contrib import admin
from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'host', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'start_time')
    search_fields = ('title', 'host__email')