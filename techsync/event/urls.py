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

    path('event_detail/<str:pk>/', views.event_detail, name='event-detail'),

    path('organizer_profile/<str:pk>/', views.organizerProfile, name='organizer-profile'),

    path('update-event/<str:pk>', views.updateEvent, name='update-event'),
    path('delete-event/<str:pk>', views.deleteEvent, name='delete-event'),

    # event list
    path('', views.events, name='events'),

    # register for event
    path('register-for-event/<str:pk>', views.registerForEvent, name='register-for-event'),

    # analytics for event
    path('analytics/<str:pk>', views.event_analytics, name='event-analytics'),

]