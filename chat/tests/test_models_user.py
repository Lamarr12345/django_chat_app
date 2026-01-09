from django.test import TestCase
from .. import models
from django.core.exceptions import ValidationError


class TestUser(TestCase):

    def setUp(self):
        self.username = "test"
        self.email = "test@email.com"
        self.password = "Test1234"
    
    def test_models_user_create(self):

        user = models.User.objects.create_user(username=self.username, email=self.email, password=self.password)
        
        self.assertEqual(self.username, user.username)
        self.assertEqual(self.email, user.email)
        self.assertNotEqual(self.password, user.password)

    def test_models_user_username_too_long(self):
        with self.assertRaises(Exception) as e:
            models.User.objects.create_user(username="a"*256, email=self.email, password=self.password)
        self.assertEqual(type(e.exception), ValidationError)

    def test_models_user_username_not_unique(self):
        models.User.objects.create_user(username=self.username, email=self.email, password=self.password)
        with self.assertRaises(Exception) as e:
            models.User.objects.create_user(username=self.username, email="a" + self.email, password=self.password)
        self.assertEqual(type(e.exception), ValidationError)

    def test_models_user_email_not_unique(self):
        models.User.objects.create_user(username=self.username, email=self.email, password=self.password)
        with self.assertRaises(Exception) as e:
            models.User.objects.create_user(username=self.username + "a", email=self.email, password=self.password)
        self.assertEqual(type(e.exception), ValidationError)