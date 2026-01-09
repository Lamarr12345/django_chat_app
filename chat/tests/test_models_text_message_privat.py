from django.test import TestCase
from .. import models
from django.core.exceptions import ValidationError


class TestTextMessagePrivat(TestCase):
    
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
        self.user3 = models.User.objects.create_user(
            username = 'test3',
            email = 'test3@gmail.com',
            password = 'Test1234'
        )
        self.url_id = f"{self.user.id}-{self.user2.id}"
        self.private_chat = models.ChatRoomPrivat.objects.create(user_1=self.user,
                                                            user_2=self.user2,
                                                            url_id=self.url_id)
        
    def test_models_text_message_privat_create_entry(self):
        test_text = "test text" 
        private_text = models.TextMessagePrivat.objects.create(content= test_text,
                                                                chat_room = self.private_chat,
                                                                user = self.user)
        
        self.assertEqual(test_text, private_text.content)
        self.assertEqual(self.private_chat, private_text.chat_room)
        self.assertEqual(self.user, private_text.user)

    def test_models_text_message_privat_not_member(self):
        test_text = "test text" 
        with self.assertRaises(Exception) as e:
            models.TextMessagePrivat.objects.create(content= test_text,
                                                                chat_room = self.private_chat,
                                                                user = self.user3)
        self.assertEqual(type(e.exception), ValidationError)

    def test_models_text_message_privat_delete_room(self):
        test_text = "test text" 
        private_text = models.TextMessagePrivat.objects.create(content= test_text,
                                                                chat_room = self.private_chat,
                                                                user = self.user)    

        self.private_chat.delete()
        self.assertFalse(models.TextMessagePrivat.objects.filter(id=private_text.id).exists())

    def test_models_text_message_privat_delete_user(self):
        test_text = "test text" 
        private_text = models.TextMessagePrivat.objects.create(content= test_text,
                                                                chat_room = self.private_chat,
                                                                user = self.user) 
        self.user.delete()
        self.assertEqual(len(models.TextMessagePrivat.objects.filter(id=private_text.id)), 0)
