# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('chat/', views.chatbot_view, name='chat_view'),
]
