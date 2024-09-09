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



# class EventForm(ModelForm):
#     class Meta:
#         model = Event
#         fields = ['title', 'description', 'date', 'end_date', 'location', 'category', 'event_image', 'speakers']
#         widgets = {
#             'title': TextInput(attrs={'class': 'input', 'placeholder': 'Enter event title'}),
#             'description': Textarea(attrs={'class': 'textarea', 'placeholder': 'Enter event description'}),
#             'date': DateTimeInput(attrs={'class': 'input', 'placeholder': 'Enter event date', 'type': 'datetime-local'}),
#             'end_date': DateTimeInput(attrs={'class': 'input', 'placeholder': 'Enter event end date', 'type': 'datetime-local'}),
#             'location': TextInput(attrs={'class': 'input', 'placeholder': 'Enter event location'}),
#             'category': SelectMultiple(attrs={'class': ' selectize-event-categories','placeholder': 'Add catergories'}),
#             'speakers': SelectMultiple(attrs={'class': ' selectize-speakers','placeholder': 'Search Speakers username'})
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         date = cleaned_data.get('date')
#         end_date = cleaned_data.get('end_date')

#         if date and end_date:
#             if end_date < date:
#                 raise ValidationError(_('End date cannot be earlier than the event date.'))

#         return cleaned_data
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for name, field in self.fields.items():
#             if name != 'speakers' and name != 'category':
#                 field.widget.attrs.update({'class': 'input'})


from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateTimeInput, Select, SelectMultiple, NumberInput
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'end_date', 
            'category', 'event_image', 'speakers', 'location_type', 'location', 'venue_name', 'place', 
            'attendees_limit',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Enter event title'}),
            'description': Textarea(attrs={'class': 'textarea', 'placeholder': 'Enter event description'}),
            'date': DateTimeInput(attrs={'class': 'input', 'placeholder': 'Enter event date', 'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'class': 'input', 'placeholder': 'Enter event end date', 'type': 'datetime-local'}),
            'location_type': forms.Select(attrs={'class': 'input'}),
            'location': TextInput(attrs={'class': 'input', 'placeholder': 'Enter event location', 'id': 'id_location'}),
            'venue_name': TextInput(attrs={'class': 'input', 'placeholder': 'Enter venue name'}),
            'place': TextInput(attrs={'class': 'input', 'placeholder': 'Enter place details (apartment, suite, etc.)'}),
            'category': SelectMultiple(attrs={'class': 'selectize-event-categories', 'placeholder': 'Add categories'}),
            'speakers': SelectMultiple(attrs={'class': 'selectize-speakers', 'placeholder': 'Search Speakers username'}),
            'attendees_limit': NumberInput(attrs={'class': 'input', 'placeholder': 'Enter attendees limit'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        end_date = cleaned_data.get('end_date')
        location_type = cleaned_data.get('location_type')
        location = cleaned_data.get('location')

        # Ensure that location is provided for VENUE events
        if location_type == 'VENUE' and not location:
            self.add_error('location', _('Location is required for venue events.'))

        # Set default values for ONLINE events
        if location_type == 'ONLINE':
            cleaned_data['location'] = 'Online'
            cleaned_data['venue_name'] = ''
            cleaned_data['place'] = ''
            # No need to reset attendees_limit as it's not specific to location type

        # Ensure that end_date is not earlier than date
        if date and end_date:
            if end_date < date:
                raise ValidationError(_('End date cannot be earlier than the event date.'))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'input' class to all fields except 'speakers' and 'category'
        for name, field in self.fields.items():
            if name not in ['speakers', 'category']:
                field.widget.attrs.update({'class': 'input'})
