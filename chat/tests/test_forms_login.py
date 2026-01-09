from django.test import TestCase
from .. import forms
from .. import models

class TestLoginForm(TestCase):
    
    def test_forms_login_valid(self):
        user = models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        form = forms.LoginForm({
            "username" : "test",
            "password" : "Test1234",
        })

        self.assertTrue(form.is_valid())

    def test_forms_login_invalid(self):
        form = forms.LoginForm({
            "username" : "test"*100,
            "password" : "Test1234",
        })

        self.assertFalse(form.is_valid())
