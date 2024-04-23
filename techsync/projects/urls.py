from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects, name='projects'),
    path('project_detail/<str:pk>/', views.project_detail, name='project_detail'),

]