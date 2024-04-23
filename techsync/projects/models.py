from django.db import models
import uuid
# Create your models here.
class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, )
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    demo_link = models.URLField(null=True, blank=True)
    source_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_count = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # is_active = models.BooleanField(default=True)
    # image = models.ImageField(upload_to='project_images/')
    
    def __str__(self):
        return self.title


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=10, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.value + ' ' + str(self.project)


class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, )
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
