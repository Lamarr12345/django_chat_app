from django.test import TestCase
from .. import forms
from .. import models

class TestSignupForm(TestCase):
    
    def test_forms_signup_valid(self):
        form = forms.SignupForm({
            "username" : "john",
            "email" : "john@email.com",
            "password" : "John1234",
            "confirm_password" : "John1234",
        })

        self.assertTrue(form.is_valid())

    def test_forms_signup_invalid(self):
        models.User.objects.create_user(
            username = 'test',
            email = 'test@email.com',
            password = 'Test1234'
        )
        form = forms.SignupForm({
            "username" : "test",
            "email" : "test@email.com",
            "password" : "Test1234",
            "confirm_password" : "Test1234",
        })

        self.assertFalse(form.is_valid())
