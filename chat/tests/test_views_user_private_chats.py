from django.test import TestCase
from django.urls import reverse
from .. import models


class TestUserPrivateChats(TestCase):
    
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
        self.private_room = models.ChatRoomPrivat.objects.create(user_1 = self.user,
                                                                 user_2 = self.user2,
                                                                 url_id = f"{self.user.id}-{self.user2.id}")
        self.user_private_chats_url = reverse('chat:user-private-chats', kwargs={"user_id":self.user.id})

    def test_user_private_chats_get_unauthenticated_visitor(self):
        response = self.client.get(self.user_private_chats_url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'no_access.html')

    def test_user_private_chats_get_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password)

        response = self.client.get(self.user_private_chats_url)

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertContains(response, self.user2.username, status_code=200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'user_private_chats.html')
        self.client.logout()

    def test_user_private_chats_get_wrong_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password) 

        response = self.client.get(reverse('chat:user-private-chats',  kwargs={"user_id":self.user2.id}))

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user2.is_authenticated)
        self.assertTemplateUsed(response,'no_access.html')
        self.client.logout()
