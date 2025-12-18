from django.test import TestCase
from .. import views
from django.urls import reverse
from .. import models

views.home

class TestHome(TestCase):
    
    def setUp(self):
        self.user = models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        self.redirect_to_home_url = reverse('chat:redirect-to-home')
        self.home_url = reverse('chat:home')
        self.login_url = reverse('chat:login')
        self.logout_url = reverse('chat:logout')
        self.signup_url = reverse('chat:signup')
        self.user_home_url = reverse('chat:user-home')
        self.user_public_chats_url = reverse('chat:user-public-chats')
        self.user_public_chat_room_url = reverse('chat:user-public-chat-room')
        self.user_private_chats_url = reverse('chat:user-private-chats')
        self.user_private_chat_room_url = reverse('chat:user-private-chat-room')
        self.user_private_chat_room_join_url = reverse('chat:user-private-chat-room-join')
        self.user_public_chat_room_join_url = reverse('chat:user-public-chat-room-join')
        self.user_public_chat_room_close_url = reverse('chat:user-public-chat-room-close')

    def test_home(self):
        print(self.redirect_to_home_url)
        print(self.home_url)
        print(self.login_url)
        print(self.logout_url)
        print(self.signup_url)
        print(self.user_home_url)
        print(self.user_public_chats_url)
        print(self.user_public_chat_room_url)
        print(self.user_private_chats_url)
        print(self.user_private_chat_room_url)
        print(self.user_private_chat_room_join_url)
        print(self.user_public_chat_room_join_url)
        print(self.user_public_chat_room_close_url)