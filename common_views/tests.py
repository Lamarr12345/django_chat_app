from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class TestViews(TestCase):

    def test_home_redirect(self):
        response = self.client.get(reverse('common-views:home-redirect'))
        self.assertRedirects(response, reverse('chat:home'))
