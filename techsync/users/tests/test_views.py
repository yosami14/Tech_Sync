from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.views import loginUser, logoutUser, registerUser, userProfile, userAccount, download_cv
from users.utils import get_search_profile
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = get_user_model().objects.create_user(username='testuser', email='test@test.com', password='testpassword')
        

    def test_download_cv_GET(self):
        self.client.login(email='test@test.com', password='testpassword')
        response = self.client.get(reverse('download-cv'))
        self.assertEquals(response.status_code, 200) 
        print("test_download_cv_GET passed")

    def test_loginUser_POST(self):
        response = self.client.post(self.login_url, {
            'email': 'test@test.com',
            'password': 'testpassword'
        })

        self.assertEquals(response.status_code, 302) 
        self.assertRedirects(response, reverse('profiles'))
        print("test_loginUser_POST passed")

    def test_logoutUser_GET(self):
        self.client.login(email='test@test.com', password='testpassword')
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 302) 
        self.assertRedirects(response, reverse('login'))
        print("test_logoutUser_GET passed")
    
    def test_Profiles_GET(self):
        response = self.client.get(reverse('profiles'))

        self.assertEquals(response.status_code, 200)  # Should be a successful request
        self.assertQuerysetEqual(response.context['profiles'], get_search_profile(''))  # Check that the profiles are correct
        self.assertEquals(response.context['search_query'], '')  # Check that the search query is correct
        # Add more assertions here to check the other context data
        print("test_Profiles_GET passed")

    def test_userProfile_GET(self):
        response = self.client.get(reverse('user-profile', args=[self.user.profile.id]))

        self.assertEquals(response.status_code, 200)  # Should be a successful request
        self.assertEquals(response.context['profile'], self.user.profile)  # Check that the profile is correct
        # Add more assertions here to check the other context data
        print("test_userProfile_GET passed")

    def test_userAccount_GET(self):
        self.client.login(email='test@test.com', password='testpassword')
        response = self.client.get(reverse('user-account'))

        self.assertEquals(response.status_code, 200)  # Should be a successful request
        self.assertEquals(response.context['profile'], self.user.profile)  # Check that the profile is correct
        # Add more assertions here to check the other context data
        print("test_userAccount_GET passed")

