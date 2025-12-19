from django.test import TestCase
from .. import views
from django.urls import reverse
from .. import models
from django.contrib.auth import authenticate
from django.contrib.auth import login

views.home

class TestHome(TestCase):
    
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

        self.password = 'Test1234'
        self.home_url = reverse('chat:home')
        self.user_home_url = reverse('chat:user-home', kwargs={"user_id":self.user.id})

    def test_home_get_unauthenticated_visitor(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'home.html')


    def test_home_get_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password) 

        response = self.client.get(self.home_url)

        session = self.client.session
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, self.user_home_url)
