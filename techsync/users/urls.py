from django.urls import path
from . import views

urlpatterns = [
    #Authentication
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    #User Creation
    path('register/', views.registerUser, name='register'),
    
    #Profile
    path('', views.Profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('account/', views.userAccount, name='user-account'),
    path('edit-account/', views.editAccount, name='edit-account'),
]