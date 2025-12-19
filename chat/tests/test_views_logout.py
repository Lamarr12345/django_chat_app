from django.test import TestCase
from .. import views
from .. import models


class TestLogout(TestCase):
    
    def setUp(self):
        self.user = models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        self.password = 'Test1234'
