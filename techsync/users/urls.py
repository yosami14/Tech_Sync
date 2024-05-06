from django.urls import path
from . import views

urlpatterns = [
    #Authentication
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.Profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
]