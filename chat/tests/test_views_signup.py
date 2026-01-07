from django.test import TestCase
from django.urls import reverse
from .. import models

class TestSignup(TestCase):
    def setUp(self):
        self.user = models.User.objects.create_user(
            username = 'test',
            email = 'test@gmail.com',
            password = 'Test1234'
        )
        self.new_username = 'test_new'
        self.new_email = 'test_new@gmail.com'
        self.password = 'Test1234'
        self.signup_url = reverse('chat:signup')

    def test_signup_get_vistor(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'signup.html')

    
    def test_signup_post_username_missing(self):
        response = self.client.post(self.signup_url, {
            "username" : "",
            "email" : self.new_email,
            "password" : self.password,
            "confirm_password" : self.password,
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'signup.html')


    def test_signup_post_email_missing(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : "",
            "password" : self.password,
            "confirm_password" : self.password,
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'signup.html')


    def test_signup_post_password_missing(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.new_email,
            "password" : "",
            "confirm_password" : self.password,
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'signup.html')


    def test_signup_post_confirm_password_missing(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.new_email,
            "password" : self.password,
            "confirm_password" : "",
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'signup.html')

    
    def test_signup_post_username_taken(self):
        response = self.client.post(self.signup_url, {
            "username" : self.user.username,
            "email" : self.new_email,
            "password" : self.password,
            "confirm_password" : self.password,
        })

        self.assertContains(response, "Username already taken.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_email_taken(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.user.email,
            "password" : self.password,
            "confirm_password" : self.password,
        })

        self.assertContains(response, "Username already taken.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_email_taken(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.user.email,
            "password" : self.password,
            "confirm_password" : self.password,
        })

        self.assertContains(response, "Email already taken.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_email_taken(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.user.email,
            "password" : self.password,
            "confirm_password" : self.password,
        })

        self.assertContains(response, "Email already taken.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_confirm_password_not_match(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.new_email,
            "password" : self.password,
            "confirm_password" : self.password +"f",
        })

        self.assertContains(response, "Password and password confirmation do not match.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_password_too_short(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.new_email,
            "password" : "Test123",
            "confirm_password" : "Test123",
        })

        self.assertContains(response, "Password shorter than 8 symbols.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_password_no_upper(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.new_email,
            "password" : "test1234",
            "confirm_password" : "test1234",
        })

        self.assertContains(response, "Password must contain upper case letter.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_password_no_lower(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.new_email,
            "password" : "TEST1234",
            "confirm_password" : "TEST1234",
        })

        self.assertContains(response, "Password must contain lower case letter.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_password_no_number(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.new_email,
            "password" : "TestTest",
            "confirm_password" : "TestTest",
        })

        self.assertContains(response, "Password must contain number.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')

    def test_signup_post_password_has_empty_space(self):
        response = self.client.post(self.signup_url, {
            "username" : self.new_username,
            "email" : self.new_email,
            "password" : " Test 1234",
            "confirm_password" : " Test 1234",
        })

        self.assertContains(response, "Password contains empty spaces.", status_code=200)
        self.assertTemplateUsed(response,'signup.html')


