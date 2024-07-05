from django.db import models
from users.models import User, EventModerator, EventOrganizer,Profile
import uuid

class EventCategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE)
    category = models.ManyToManyField(EventCategory, blank=True)
    event_image = models.ImageField(upload_to='events', default='default_event.png')
    attendees = models.ManyToManyField(User, blank=True, related_name='attending_events')
    speakers = models.ManyToManyField(Profile, blank=True, related_name='speaking_events')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_by = models.ForeignKey(EventModerator, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_events')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title


