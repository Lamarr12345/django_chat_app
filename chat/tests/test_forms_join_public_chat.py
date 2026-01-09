from django.test import TestCase
from .. import forms
from .. import models

class TestJoinPublicChatForm(TestCase):
    
    def test_forms_join_public_chat_valid(self):
        user = models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        models.ChatRoomPublic.objects.create(name="test room", url_id="00000001", owner=user)
        form = forms.JoinPublicChatForm({
            "chat_id" : "00000001",
        })

        self.assertTrue(form.is_valid())

    def test_forms_join_public_chat_invalid(self):
        form = forms.JoinPublicChatForm({
            "chat_id" : "any",
        })

        self.assertFalse(form.is_valid())
