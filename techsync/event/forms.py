from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from users.models import EventOrganizer, EventModerator
from event.models import Event
from django.forms import ModelForm, TextInput, Textarea, DateTimeInput, Select, SelectMultiple, DateInput, ImageField
from django.core.exceptions import ValidationError
from .models import EventCategory
from django.utils.translation import gettext_lazy as _
class OrganizerForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Full Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})

#used to edit user profile
class ProfileForm(ModelForm):
    class Meta:
        model = EventOrganizer
        fields = '__all__'
        exclude = ('user', 'status', 'verified')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'end_date', 'location', 'category', 'event_image', 'speakers']
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Enter event title'}),
            'description': Textarea(attrs={'class': 'textarea', 'placeholder': 'Enter event description'}),
            'date': DateTimeInput(attrs={'class': 'input', 'placeholder': 'Enter event date', 'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'class': 'input', 'placeholder': 'Enter event end date', 'type': 'datetime-local'}),
            'location': TextInput(attrs={'class': 'input', 'placeholder': 'Enter event location'}),
            'category': SelectMultiple(attrs={'class': ' selectize-event-categories','placeholder': 'Add catergories'}),
            'speakers': SelectMultiple(attrs={'class': ' selectize-speakers','placeholder': 'Search Speakers username'})
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        end_date = cleaned_data.get('end_date')

        if date and end_date:
            if end_date < date:
                raise ValidationError(_('End date cannot be earlier than the event date.'))

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'speakers' and name != 'category':
                field.widget.attrs.update({'class': 'input'})