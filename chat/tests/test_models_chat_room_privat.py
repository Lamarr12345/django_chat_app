from django.test import TestCase
from .. import models
from django.db.utils import IntegrityError


class TestChatRoomPrivat(TestCase):

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
        self.url_id = f"{self.user.id}-{self.user2.id}"
    
    def test_chat_room_privat_create(self):
        private_chat = models.ChatRoomPrivat.objects.create(user_1=self.user,
                                                            user_2=self.user2,
                                                            url_id=self.url_id)
        
        self.assertTrue(models.ChatRoomPrivat.objects.filter(url_id=self.url_id).exists())
        self.assertEqual(private_chat.user_1, self.user)
        self.assertEqual(private_chat.user_2, self.user2)
        self.assertEqual(private_chat.url_id, self.url_id)
        self.assertEqual(private_chat.state, 1)

    def test_chat_room_privat_create_url_id_unique(self):
        models.ChatRoomPrivat.objects.create(user_1=self.user,
                                                            user_2=self.user2,
                                                            url_id=self.url_id)
        self.assertTrue(models.ChatRoomPrivat.objects.filter(url_id=self.url_id).exists())

        with self.assertRaises(Exception) as ie:
            models.ChatRoomPrivat.objects.create(user_1=self.user,
                                                            user_2=self.user2,
                                                            url_id=self.url_id)
        self.assertEqual(type(ie.exception), IntegrityError)
