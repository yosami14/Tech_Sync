from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.forms import ModelForm
from .models import Skill,Message
from django import forms
class UserForm(UserCreationForm):
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

# # Event Organizer User Form
# class EventOrganizerUserForm(UserCreationForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['first_name', 'username', 'email', 'password1', 'password2']
#         labels = {
#             'first_name': 'Full Name',
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for name, field in self.fields.items():
#                 field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            if name == 'phone_number':
                field.widget.attrs.update({
                    'placeholder': "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
                })



class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        
        # Add the class 'skill-select' to the 'name' field
        self.fields['name'].widget.attrs.update({'class': 'input skill-select', 'placeholder': 'Search for a skill...'})


class InboxForm(ModelForm):
    class Meta:
        model = Message
        fields = ['senderName', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super(InboxForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})