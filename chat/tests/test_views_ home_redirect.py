from django.test import TestCase
from .. import views
from django.urls import reverse


class TestHomeRedirect(TestCase):
    
    def test_home_redirect(self):
        response = self.client.get(reverse('chat:redirect-to-home'))
        self.assertRedirects(response, reverse('chat:home'))
