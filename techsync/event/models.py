from django.db import models
from users.models import User, EventModerator, EventOrganizer,Profile
import uuid
#from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
class EventCategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# class Event(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
#     title = models.CharField(max_length=255)
#     # description = models.TextField()
#     description = RichTextField()
#     date = models.DateTimeField()
#     end_date = models.DateTimeField(blank=True, null=True)
#     location = models.CharField(max_length=255)
#     organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE)
#     category = models.ManyToManyField(EventCategory, blank=True)
#     event_image = models.ImageField(upload_to='events', default='default_event.png')
#     attendees = models.ManyToManyField(User, blank=True, related_name='attending_events')
#     speakers = models.ManyToManyField(Profile, blank=True, related_name='speaking_events')

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     verified_by = models.ForeignKey(EventModerator, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_events')
#     is_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title


class Event(models.Model):
    LOCATION_CHOICES = [
        ('VENUE', 'Venue'),
        ('ONLINE', 'Online'),
    ]
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = RichTextField()
    date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location_type = models.CharField(max_length=6, choices=LOCATION_CHOICES, default='VENUE')
    location = models.CharField(max_length=255, blank=True, null=True)
    venue_name = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE)
    category = models.ManyToManyField(EventCategory, blank=True)
    event_image = models.ImageField(upload_to='events', default='default_event.png')
    #attendees = models.ManyToManyField(User, blank=True, related_name='attending_events')
    attendees = models.ManyToManyField(User, through='EventRegistration', related_name='attending_events')
    attendees_limit = models.PositiveIntegerField(default=10)
    speakers = models.ManyToManyField(Profile, blank=True, related_name='speaking_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_by = models.ForeignKey(EventModerator, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_events')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.location_type == 'VENUE' and not self.location:
            raise ValidationError('Location is required for venue events.')
        if self.location_type == 'ONLINE':
            self.location = 'Online'
            self.venue_name = ''
            self.place = ''



class EventRegistration(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    has_attended = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'attendee')

    def __str__(self):
        return f'{self.event.title} - {self.attendee.username}'