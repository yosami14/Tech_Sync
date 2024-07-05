from django.urls import path
from . import views

urlpatterns = [

    path('register-organizer/', views.registerOrganizer, name='register-organizer'),

    # path('account/', views.userAccount, name='user-account'),

    path('edit-organizer-profile/', views.editAccount, name='edit-organizer-profile'),
    path('organization-account/', views.userAccount, name='organization-account'),
    path('add-event/', views.addEvent, name='add-event'),
    
    #selectize
    path('get_speakers/', views.get_speakers, name='get_speakers'),
    path('get_event_categories/', views.get_speakers, name='get_event_categories'),
]