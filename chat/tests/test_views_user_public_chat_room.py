from django.test import TestCase
from django.urls import reverse
from .. import models

class TestUserPublicChatRoom(TestCase):
    
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
        self.user_public_chat_room_url = reverse('chat:user-public-chat-room', kwargs={"user_id":self.user.id, "url_id": self.public_chat.url_id})

    def test_user_public_chat_room_get_unauthenticated_visitor(self):
        response = self.client.get(self.user_public_chat_room_url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'no_access.html')

    def test_user_public_chat_room_get_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.get(self.user_public_chat_room_url)

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'user_public_chat_room.html')
        self.client.logout()

    def test_user_public_chat_room_get_wrong_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password) 

        response = self.client.get(reverse('chat:user-public-chat-room',  kwargs={"user_id":self.user2.id, "url_id": self.public_chat.url_id}))

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user2.is_authenticated)
        self.assertTemplateUsed(response,'no_access.html')
        self.client.logout()

    def test_user_public_chat_room_get_not_member_user(self):
        self.client.login(username=self.user2.username,password=self.password)

        response = self.client.get(self.user_public_chat_room_url)

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user2.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user2.is_authenticated)
        self.assertTemplateUsed(response,'no_access.html')
        self.client.logout()

    def test_user_public_chat_room_post_send_message(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.post(self.user_public_chat_room_url, {
            "text" : "this is test text",
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertContains(response, "this is test text", status_code=200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'user_public_chat_room.html')
        self.client.logout()

    def test_user_public_chat_room_post_send_message_in_closed_room(self):
        self.client.login(username=self.user.username,password=self.password)

        self.public_chat.state = 0
        self.public_chat.save()

        response = self.client.post(self.user_public_chat_room_url, {
            "text" : "this is test text",
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'no_access.html')
        self.client.logout()

