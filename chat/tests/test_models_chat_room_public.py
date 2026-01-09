from django.test import TestCase
from .. import models
from django.core.exceptions import ValidationError


class TestChatRoomPublic(TestCase):
    
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
        self.url_id = "00000001"
    
    def test_chat_room_public_create(self):
        public_chat = models.ChatRoomPublic.objects.create(name="test name", url_id=self.url_id, owner=self.user)
        public_chat.user.add(self.user)
        
        self.assertTrue(models.ChatRoomPublic.objects.filter(url_id=self.url_id).exists())
        self.assertTrue(public_chat.user.filter(pk=self.user.id).exists())
        self.assertFalse(public_chat.user.filter(pk=self.user2.id).exists())
        self.assertEqual(public_chat.url_id, self.url_id)
        self.assertEqual(public_chat.state, 1)
        self.assertEqual(public_chat.owner, self.user)

    def test_chat_room_public_create_url_id_unique(self):
        models.ChatRoomPublic.objects.create(name="test name", url_id=self.url_id, owner=self.user)
        self.assertTrue(models.ChatRoomPublic.objects.filter(url_id=self.url_id).exists())

        with self.assertRaises(Exception) as e:
            models.ChatRoomPublic.objects.create(name="test name", url_id=self.url_id, owner=self.user)
        self.assertEqual(type(e.exception), ValidationError)

