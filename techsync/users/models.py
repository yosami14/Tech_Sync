from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid



class User(AbstractUser):
    email = models.EmailField(unique=True)
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

# def profileUpdated(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()



