# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('chat/', views.chatbot_view, name='chat_view'),
    path('telegram-to-gemini/', views.telegram_to_gemini, name='telegram_to_gemini'),
    path('register/', views.register_via_telegram, name='register_via_telegram'),
]
