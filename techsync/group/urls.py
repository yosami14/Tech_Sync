from django.urls import path
from . import views

urlpatterns = [


    path('', views.home, name="home-group"),
    path('room/<str:pk>/', views.room, name="room"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    
    
    # path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    #setting
    path('manage-group/<str:pk>', views.manage_group, name="manage-group"),
    path('leave-group/<str:pk>', views.leave_group, name="leave-group"),
    # File input
    path('room/fileupload/<str:pk>', views.room_file_upload, name="room-file-upload"),

]   
