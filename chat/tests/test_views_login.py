from django.test import TestCase
from django.urls import reverse
from .. import models

class TestLogin(TestCase):
    
    def setUp(self):
        self.user = models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        self.password = 'Test1234'
        self.login_url = reverse('chat:login')
        self.user_home_url = reverse('chat:user-home', kwargs={"user_id":self.user.id})


    def test_login_get_visitor(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'login.html')


    def test_login_post_login_valid_user(self):
        response = self.client.post(self.login_url, {
            "username" : self.user.username,
            "password" : self.password, 
        })
        session = self.client.session
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(session['_auth_user_id']), str(self.user.id))
        self.assertRedirects(response, self.user_home_url)
        self.client.logout()
        

    def test_login_post_invalid_username(self):
        response = self.client.post(self.login_url, {
            "username" : self.user.username + "f",
            "password" : self.password, 
        })
        session = self.client.session
        self.assertNotIn('_auth_user_id', session)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'login.html')

    def test_login_post_invalid_password(self):
        response = self.client.post(self.login_url, {
            "username" : self.user.username,
            "password" : self.password + "f", 
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response,'login.html')
