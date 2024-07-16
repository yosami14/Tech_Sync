"""
URL configuration for techsync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/',include('projects.urls')),
    path('group/',include('group.urls')),
    path('chatroom/',include('a_rtchat.urls')),
    path('event/',include('event.urls')),
    path('',include('users.urls')),

    path('admin-charts/', views.admin_dashboard, name='admin-charts'),
    

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="main/reset_password.html"),
        name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="main/reset_password_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/reset.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="main/reset_password_complete.html"),
         name="password_reset_complete"),

    #ADMIN CHARTS
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)