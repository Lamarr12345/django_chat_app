from django.test import TestCase
from .. import forms

class TestChatInputForm(TestCase):
    
    def test_forms_chat_input_valid(self):
        form = forms.ChatInputForm({
            "text" : "a",
        })

        self.assertTrue(form.is_valid())

    def test_forms_chat_input_invalid(self):
        form = forms.ChatInputForm({
            "text" : "a"*256,
        })


        self.assertFalse(form.is_valid())
