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

    #skill
    path('add-skill/', views.createSkill, name="add-skill"),
    path('get_skills/', views.get_skills, name='get_skills'),
    path('update-skill/<str:pk>/', views.updateSkill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.deleteSkill, name="delete-skill"),

    #Inbox
    path('inbox/', views.inbox, name='inbox'),
    path('inbox-message/<str:pk>', views.viewInbox, name='inbox-message'),
    path('send-inbox/<str:pk>', views.createInbox, name='create-inbox'),

]
