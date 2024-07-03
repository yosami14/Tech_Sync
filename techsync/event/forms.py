from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from users.models import EventOrganizer,EventModerator
from django.forms import ModelForm
from django import forms
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