from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import Project
# python manage.py test projects.tests.ProjectsViewTest
# This test case is for the ProjectsView.
class ProjectsViewTest(TestCase):
    # This setup function runs before each test. It creates a test client and some test projects.
    def setUp(self):
        self.client = Client()
        self.projects_url = reverse('projects')

        # Create some test projects
        Project.objects.create(title='Test Project 1', description='This is test project 1.')
        Project.objects.create(title='Test Project 2', description='This is test project 2.')
        Project.objects.create(title='Test Project 3', description='This is test project 3.')

    # This test checks if the projects view is working correctly.
    def test_projects_view(self):
        # Send a GET request to the projects view.
        response = self.client.get(self.projects_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the number of projects in the context is correct
        self.assertEqual(len(response.context['projects']), 3)

        # Check if the titles of the projects are correct
        project_titles = [project.title for project in response.context['projects']]
        self.assertIn('Test Project 1', project_titles)
        self.assertIn('Test Project 2', project_titles)
        self.assertIn('Test Project 3', project_titles)


from django.test import TestCase, Client
from django.urls import reverse
from .models import Project


# python manage.py test projects.tests.ProjectsViewSearch
class ProjectsViewSearch(TestCase):
    def setUp(self):
        # Create a client to make requests
        self.client = Client()
        # Get the URL for the 'projects' view
        self.projects_url = reverse('projects')

        # Create some test projects
        # 'Techsync' and 'Techsync 2' are Django projects
        # 'Techsync Project' is not a Django project
        Project.objects.create(title='Techsync', description='This is a Django project.')
        Project.objects.create(title='Techsync 2', description='This is another Django project.')
        Project.objects.create(title='Techsync Project', description='This is not a Django project.')

    def test_projects_view_with_search_query(self):
        # Send a GET request to the 'projects' view with 'Techsync' as the search query
        response = self.client.get(self.projects_url, {'search_query': 'Techsync'})

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the number of projects in the context is correct
        # Since all projects have 'Techsync' in their title, all should be returned
        self.assertEqual(len(response.context['projects']), 3)

        # Check if the titles of the projects are correct
        # Since all projects have 'Techsync' in their title, all should be in the list of project titles
        project_titles = [project.title for project in response.context['projects']]
        self.assertIn('Techsync', project_titles)
        self.assertIn('Techsync 2', project_titles)
        self.assertIn('Techsync Project', project_titles)