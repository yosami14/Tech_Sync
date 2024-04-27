from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project_detail/<str:pk>/', views.project_detail, name='project_detail'),
    path('create-project/', views.createProject, name='create-project'),
    path('update-project/<str:pk>', views.updateProject, name='update-project'),
    path('delete-project/<str:pk>', views.deleteProject, name='delete-template'),
    
]