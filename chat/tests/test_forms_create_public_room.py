from django.test import TestCase
from .. import forms

class TestCreatePublicRoomForm(TestCase):
    
    def test_forms_create_public_room_valid(self):
        form = forms.CreatePublicRoomForm({
            "name" : "a",
        })

        self.assertTrue(form.is_valid())

    def test_forms_create_public_room_invalid(self):
        form = forms.CreatePublicRoomForm({
            "name" : "a"*256,
        })

        self.assertFalse(form.is_valid())


