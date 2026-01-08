from django.test import TestCase
from django.urls import reverse
from .. import models


class TestUserPublicChatRoomClose(TestCase):
    
    def setUp(self):
        self.user = models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        self.user2 = models.User.objects.create_user(
            username = 'test2',
            email = 'test2@gmail.com',
            password = 'Test1234'
        )
        self.password = 'Test1234'
        self.public_chat = models.ChatRoomPublic.objects.create(name="test room", url_id="00000001", owner=self.user)
        self.public_chat.user.add(self.user)
        self.user_public_chat_room_close_url = reverse('chat:user-public-chat-room-close', kwargs={"user_id":self.user.id, "url_id": self.public_chat.url_id})
        self.user_public_chats_url = reverse('chat:user-public-chats', kwargs={"user_id":self.user.id})

    def test_user_public_chat_room_close_get_unauthenticated_visitor(self):
        response = self.client.get(self.user_public_chat_room_close_url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'no_access.html')

    def test_user_public_chat_room_close_get_correct_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.get(self.user_public_chat_room_close_url)

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ChatRoomPublic.objects.get(id=self.public_chat.id).state, 0)
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, self.user_public_chats_url)
        self.client.logout()

    def test_user_public_chat_room_close_get_wrong_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password) 

        response = self.client.get(reverse('chat:user-public-chat-room-close',  kwargs={"user_id":self.user2.id, "url_id": self.public_chat.url_id}))

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user2.is_authenticated)
        self.assertTemplateUsed(response,'no_access.html')
        self.client.logout()

