from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path('', views.home_redirect, name='redirect-to-home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('<int:user_id>/home/', views.user_home, name='user-home'),
    path('<int:user_id>/public_chats/', views.user_public_chats, name='user-public-chats'),
    path('<int:user_id>/public_chat/<str:url_id>/', views.user_public_chat_room, name='user-public-chat-room'),
    path('<int:user_id>/privat_chats/', views.user_private_chats, name='user-private-chats'),
    path('<int:user_id>/privat_chat/<str:url_id>/', views.user_private_chat_room, name='user-private-chat-room'),
    path('<int:user_id>/privat_chat/<str:url_id>/join', views.user_private_chat_room_join, name='user-private-chat-room-join'),
]
