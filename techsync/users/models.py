from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps as django_apps
import uuid



class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_event_organizer = models.BooleanField(default=False)
    is_event_moderator = models.BooleanField(default=False)
    is_speaker = models.BooleanField(default=False)  # Flag to identify if user is a speaker

    is_recruiter = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    has_resume = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, )
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200, blank=True,null=True)
    username = models.CharField(max_length=200, blank=True,null=True,unique=True)
    headline = models.CharField(max_length=200, blank=True,null=True)
    about = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True,null=True)
    profile_image = models.ImageField(null=True, blank=True,upload_to='profiles', default='default_profile.png')
    github_link = models.CharField(max_length=200, blank=True,null=True)
    twitter_link = models.CharField(max_length=200, blank=True,null=True)
    linkedin_link = models.CharField(max_length=200, blank=True,null=True)
    personal_link = models.CharField(max_length=200, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # or add feature that lets user create there own link

    def __str__(self):
        return str(self.user.username)
    
class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)
    



class EventModerator(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    assigned_events = models.ManyToManyField('event.Event', blank=True, related_name='assigned_moderators')
    profile_image = models.ImageField(null=True, blank=True, upload_to='moderators', default='default_moderator.png')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or self.user.username}"

#Audit there actions
class ModerationHistory(models.Model):
    moderator = models.ForeignKey(EventModerator, on_delete=models.CASCADE, related_name='moderation_history')
    action_timestamp = models.DateTimeField(auto_now_add=True)
    action_description = models.TextField()

    def __str__(self):
        return f"{self.moderator.user.username} - {self.action_timestamp}"


class EventOrganizer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='organizers', default='default_organizer.png')
    verified = models.BooleanField(default=False)
    twitter_link = models.CharField(max_length=200, blank=True, null=True)
    linkedin_link = models.CharField(max_length=200, blank=True, null=True)
    facebook_link = models.CharField(max_length=200, blank=True, null=True)
    more_link = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.organization_name
    



class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, )
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True, blank=True, related_name='messages')
    senderName = models.CharField(max_length=200, blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True,null=True)
    subject = models.CharField(max_length=200, blank=True,null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.senderName)
    
    class Meta:
        ordering = ['-created_at']

def profileUpdated(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
