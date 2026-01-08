from django.test import TestCase
from django.urls import reverse
from .. import models


class TestUserPublicChats(TestCase):
    
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
        self.user_public_chats_url = reverse('chat:user-public-chats', kwargs={"user_id":self.user.id})

    def test_user_public_chats_get_unauthenticated_visitor(self):
        response = self.client.get(self.user_public_chats_url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'no_access.html')

    def test_user_public_chats_get_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.get(self.user_public_chats_url)

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'user_public_chats.html')
        self.client.logout()

    def test_user_public_chats_get_wrong_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password) 

        response = self.client.get(reverse('chat:user-public-chats',  kwargs={"user_id":self.user2.id}))

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user2.is_authenticated)
        self.assertTemplateUsed(response,'no_access.html')
        self.client.logout()

    def test_user_public_chats_get_invalid_order_param(self):
        self.client.login(username=self.user.username,password=self.password) 

        response = self.client.get(reverse('chat:user-public-chats',  kwargs={"user_id":self.user.id}) + "?order=reverse")

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user2.is_authenticated)
        self.assertTemplateUsed(response,'user_public_chats.html')
        self.client.logout()

    def test_user_public_chats_post_create_public_room(self):
        self.client.login(username=self.user.username,password=self.password) 

        response = self.client.post(self.user_public_chats_url, {
            "name" : "this is a test room",
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertContains(response, "this is a test room", status_code=200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'user_public_chats.html')
        self.client.logout()

    def test_user_public_chats_post_user_room_limit(self):
        self.client.login(username=self.user.username,password=self.password) 

        new_chat1 = models.ChatRoomPublic.objects.create(name="test room 1", url_id="1", owner=self.user)
        new_chat1.user.add(self.user)
        new_chat2 = models.ChatRoomPublic.objects.create(name="test room 2", url_id="2", owner=self.user)
        new_chat2.user.add(self.user)
        new_chat3 = models.ChatRoomPublic.objects.create(name="test room 3", url_id="3", owner=self.user)
        new_chat3.user.add(self.user)

        response = self.client.post(self.user_public_chats_url, {
            "name" : "this is a test room",
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertContains(response, "User has too many open rooms.", status_code=200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'user_public_chats.html')
        self.client.logout()