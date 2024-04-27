from django.forms import ModelForm
from .models import Project, Tag
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags', 'image']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'selectize-tags'}),
        }
        