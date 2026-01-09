from django.test import TestCase
from .. import forms
from .. import models


class TestJoinPrivateChatForm(TestCase):
    
    def test_forms_join_private_chat_valid(self):
        models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        form = forms.JoinPrivateChatForm({
            "username" : "test",
        })

        self.assertTrue(form.is_valid())

    def test_forms_join_private_chat_invalid(self):
        form = forms.JoinPrivateChatForm({
            "username" : "any",
        })

        self.assertFalse(form.is_valid())
