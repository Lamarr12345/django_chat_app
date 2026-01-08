from django.test import TestCase
from django.urls import reverse
from .. import models


class TestUserHome(TestCase):

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
        self.user_home_url = reverse('chat:user-home', kwargs={"user_id":self.user.id})
        self.public_chat = models.ChatRoomPublic.objects.create(name="test room", url_id="00000001", owner=self.user)

    def test_user_home_get_unauthenticated_visitor(self):
        response = self.client.get(self.user_home_url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'no_access.html')

    def test_user_home_get_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.get(self.user_home_url)

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'user_home.html')
        self.client.logout()

    def test_user_home_get_wrong_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password) 

        response = self.client.get(reverse('chat:user-home', kwargs={"user_id":self.user2.id}))

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user2.is_authenticated)
        self.assertTemplateUsed(response,'no_access.html')
        self.client.logout()

    def test_user_home_post_open_public_chats(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.post(self.user_home_url, {
            "form-type" : "public-chat-rooms",
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, reverse("chat:user-public-chats", kwargs={"user_id":self.user.id}))
        self.client.logout()

    def test_user_home_post_join_public_chat(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.post(self.user_home_url, {
            "form-type" : "join-public-chat-room",
            "chat_id" : self.public_chat.url_id,
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, reverse("chat:user-public-chat-room", kwargs={"user_id":self.user.id, "url_id": self.public_chat.url_id}))
        self.client.logout()

    def test_user_home_post_join_public_chat_wrong_id(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.post(self.user_home_url, {
            "form-type" : "join-public-chat-room",
            "chat_id" : "00000002",
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertContains(response, "Chat ID not found.", status_code=200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed("user_home.html")
        self.client.logout()

    def test_user_home_post_join_public_chat_closed(self):
        self.client.login(username=self.user.username,password=self.password)

        self.public_chat.state = 0
        self.public_chat.save()
        response = self.client.post(self.user_home_url, {
            "form-type" : "join-public-chat-room",
            "chat_id" : self.public_chat.url_id,
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertContains(response, "Chat Room has been closed.", status_code=200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed("user_home.html")
        self.client.logout()

    def test_user_home_post_open_private_chats(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.post(self.user_home_url, {
            "form-type" : "private-chat-rooms",
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, reverse("chat:user-private-chats", kwargs={"user_id":self.user.id}))
        self.client.logout()

    def test_user_home_post_join_private_chat(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.post(self.user_home_url, {
            "form-type" : "join-private-chat-room",
            "username" : self.user2.username,
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, reverse("chat:user-private-chat-room", kwargs={"user_id":self.user.id, "url_id": f"{self.user.id}-{self.user2.id}"}))
        self.client.logout()

    def test_user_home_post_join_private_chat_own_username(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.post(self.user_home_url, {
            "form-type" : "join-private-chat-room",
            "username" : self.user.username,
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertContains(response, "t be your own.</li>", status_code=200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed("user_home.html")
        self.client.logout()

    def test_user_home_post_join_private_chat_username_not_found(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.post(self.user_home_url, {
            "form-type" : "join-private-chat-room",
            "username" : "john",
        })

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertContains(response, "Username not found.", status_code=200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed("user_home.html")
        self.client.logout()