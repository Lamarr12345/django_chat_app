from django.test import TestCase
from .. import models
from django.core.exceptions import ValidationError


class TestTextMessagePublic(TestCase):
    
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
        self.public_chat = models.ChatRoomPublic.objects.create(name="test name", url_id=self.url_id, owner=self.user)
        self.public_chat.user.add(self.user)

    def test_models_text_message_public_create_entry(self):
        test_text = "test text" 
        public_text = models.TextMessagePublic.objects.create(content= test_text,
                                                                chat_room = self.public_chat,
                                                                user = self.user)
        
        self.assertEqual(test_text, public_text.content)
        self.assertEqual(self.public_chat, public_text.chat_room)
        self.assertEqual(self.user, public_text.user)

    def test_models_text_message_public_not_member(self):
        test_text = "test text" 
        with self.assertRaises(Exception) as e:
            models.TextMessagePublic.objects.create(content= test_text,
                                                                chat_room = self.public_chat,
                                                                user = self.user2)
        self.assertEqual(type(e.exception), ValidationError)

    def test_models_text_message_public_delete_room(self):
        test_text = "test text" 
        public_text = models.TextMessagePublic.objects.create(content= test_text,
                                                                chat_room = self.public_chat,
                                                                user = self.user)    

        self.public_chat.delete()
        self.assertFalse(models.TextMessagePublic.objects.filter(id=public_text.id).exists())

    def test_models_text_message_public_delete_user(self):
        test_text = "test text" 
        public_text = models.TextMessagePublic.objects.create(content= test_text,
                                                                chat_room = self.public_chat,
                                                                user = self.user) 
        self.user.delete()
        self.assertEqual(models.TextMessagePublic.objects.filter(id=public_text.id)[0].user, None)

