from django import forms
from django.core.exceptions import ValidationError
from . import models


class SignupForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    def clean(self):
        clean_data = super().clean()
        print(clean_data)
        if clean_data["password"] != clean_data["confirm_password"]:
            raise ValidationError("Password and password confirmation do not match.")
        if models.User.objects.filter(username=clean_data["username"]):
            raise ValidationError("Username already taken.")
        if models.User.objects.filter(email=clean_data["email"]):
            raise ValidationError("Email already taken.")
