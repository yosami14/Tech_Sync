from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users import views 

# run test 
# python manage.py test users.tests.test_urls

class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, views.loginUser)
        print("test_login_url_is_resolved passed")

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, views.logoutUser)
        print("test_logout_url_is_resolved passed")

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, views.registerUser)
        print("test_register_url_is_resolved passed")
        
    def test_profiles_url_is_resolved(self):
        url = reverse('profiles')
        self.assertEquals(resolve(url).func, views.Profiles)
        print("test_profiles_url_is_resolved passed")

    def test_user_profile_url_is_resolved(self):
        url = reverse('user-profile', args=['some-pk'])
        self.assertEquals(resolve(url).func, views.userProfile)
        print("test_user_profile_url_is_resolved passed")

    def test_user_account_url_is_resolved(self):
        url = reverse('user-account')
        self.assertEquals(resolve(url).func, views.userAccount)
        print("test_user_account_url_is_resolved passed")

    def test_edit_account_url_is_resolved(self):
        url = reverse('edit-account')
        self.assertEquals(resolve(url).func, views.editAccount)
        print("test_edit_account_url_is_resolved passed")