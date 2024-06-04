from django.forms import ModelForm, TextInput, Textarea, SelectMultiple
from .models import Project, Review,Tag
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags', 'image']
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Enter project title'}),
            'description': Textarea(attrs={'class': 'textarea', 'placeholder': 'Enter project description'}),
            'demo_link': TextInput(attrs={'class': 'input', 'placeholder': 'Enter demo URL'}),
            'source_link': TextInput(attrs={'class': 'input', 'placeholder': 'Enter source URL'}),
            'tags': SelectMultiple(attrs={'class': 'selectize-tags','placeholder': 'Search tags'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'tags':
                field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels = {
            'body': 'Enter your comment here',
            'value': 'Vote for this project'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})