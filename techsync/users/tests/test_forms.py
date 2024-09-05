from django.test import TestCase
from users.forms import SkillForm
from users.models import Skill
from django.contrib.auth import get_user_model
from users.forms import UserForm, ProfileForm

# run test 
# python manage.py test users.tests.test_forms

class UserFormTest(TestCase):
    def test_user_form(self):
        data = {
            'first_name': 'Test User',
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        form = UserForm(data=data)

        if not form.is_valid():
            print(form.errors)
        else:
            print("Form is valid")

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], data['first_name'])
        self.assertEqual(form.cleaned_data['username'], data['username'])
        self.assertEqual(form.cleaned_data['email'], data['email'])
        print("test_user_form passed")

class TestProfileForm(TestCase):
    def test_profile_form(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', email='test@test.com', password='testpassword')
        data = {
            'phone_number': '+1234567890',
            'name': 'Test User',
            'username': 'testusername',
            'headline': 'Test Headline',
            'about': 'This is a test about',
            'location': 'Test Location',
            # Add other fields as necessary
        }

        form = ProfileForm(data=data)

        if not form.is_valid():
            print(form.errors)
        else:
            print("Form is valid")

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['phone_number'], data['phone_number'])
        self.assertEqual(form.cleaned_data['name'], data['name'])
        self.assertEqual(form.cleaned_data['username'], data['username'])
        self.assertEqual(form.cleaned_data['headline'], data['headline'])
        self.assertEqual(form.cleaned_data['about'], data['about'])
        self.assertEqual(form.cleaned_data['location'], data['location'])
        # Add other fields as necessary
        print("test_profile_form passed")

class TestSkillForm(TestCase):
    def test_skill_form(self):
        skill = Skill.objects.create(name="Test Skill", owner=None)
        form = SkillForm(data={
            'name': skill.name,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], skill.name)
        print("test_skill_form passed")