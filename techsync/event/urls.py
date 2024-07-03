from django.urls import path
from . import views

urlpatterns = [
    # ... your other url patterns ...
    path('register-organizer/', views.registerOrganizer, name='register-organizer'),

    # path('account/', views.userAccount, name='user-account'),

    path('edit-organizer-profile/', views.editAccount, name='edit-organizer-profile'),
    path('account/', views.userAccount, name='organization-account'),
]