from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# python manage.py test users.tests.RegisterUserTest
# to create a user account
class RegisterUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register') 

    def test_register_user(self):
        # Define a dictionary with the data for the new user
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        # Send a POST request to the registerUser view with the data for the new user
        response = self.client.post(self.register_url, data)

        # Check if the response status is a redirect (302)
        self.assertEqual(response.status_code, 302)

        # Check if the user was redirected to the 'edit-account' page
        self.assertEqual(response.url, reverse('edit-account'))  # replace 'edit-account' with the actual name of the URL pattern for the edit-account view

        # Check if the user was created
        User = get_user_model()
        self.assertTrue(User.objects.filter(username=data['username']).exists())



#python manage.py test users.tests.LoginLogoutTest
# to login and logout a user test
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class LoginLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')  # replace 'login' with the actual name of the URL pattern for the loginUser view
        self.logout_url = reverse('logout')  # replace 'logout' with the actual name of the URL pattern for the logoutUser view

        # Create a test user
        self.test_user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_login_logout_user(self):
        # Define a dictionary with the data for the test user
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }

        # Send a POST request to the loginUser view with the data for the test user
        response = self.client.post(self.login_url, data)

        # Check if the response status is a redirect (302)
        self.assertEqual(response.status_code, 302)

        # Check if the user was authenticated and logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.test_user.pk)

        # Send a GET request to the logoutUser view
        response = self.client.get(self.logout_url)

        # Check if the response status is a redirect (302)
        self.assertEqual(response.status_code, 302)

        # Check if the user was logged out
        self.assertNotIn('_auth_user_id', self.client.session)