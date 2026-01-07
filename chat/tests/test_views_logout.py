from django.test import TestCase
from .. import views
from .. import models
from django.urls import reverse


class TestLogout(TestCase):
    
    def setUp(self):
        self.user = models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        self.password = 'Test1234'
        self.logout_url = reverse('chat:logout')

    def test_logout_get_authenticated_user(self):
        self.client.login(username=self.user.username,password=self.password) 

        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get(self.logout_url)
        
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'logout.html')
        self.client.logout()

    def test_logout_get_unauthenticated_visitor(self):
        response = self.client.get(self.logout_url)

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'no_access.html')



    
