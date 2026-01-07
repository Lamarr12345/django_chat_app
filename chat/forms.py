from django import forms
from django.core.exceptions import ValidationError
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    def clean(self):
        clean_data = super().clean()
        username = clean_data.get("username")
        password = clean_data.get("password")
        if not models.User.objects.filter(username=username):
            self.add_error("username", ValidationError(f"Username '{username}' not found."))
        potential_user = models.User.objects.filter(username=username)
        if potential_user:
            if not potential_user[0].check_password(password):
                self.add_error("password", ValidationError("Wrong password."))


class SignupForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))


    def clean(self):
        clean_data = super().clean()
        username = clean_data.get("username")
        email = clean_data.get("email")
        password  = clean_data.get("password")
        confirm_password = clean_data.get("confirm_password")

        if models.User.objects.filter(username=username):
            self.add_error("username", ValidationError("Username already taken."))
        if models.User.objects.filter(email=email):
            self.add_error("email", ValidationError("Email already taken."))
        if password != confirm_password:
            self.add_error("password", ValidationError("Password and password confirmation do not match."))
        if not password or len(password) < 8:
            self.add_error("password", ValidationError("Password shorter than 8 symbols."))
        if not password or not [x for x in password if x.isupper()]:
            self.add_error("password", ValidationError("Password must contain upper case letter."))
        if not password or not [x for x in password if x.islower()]:
            self.add_error("password", ValidationError("Password must contain lower case letter."))
        if not password or not [x for x in password if x.isnumeric()]:
            self.add_error("password", ValidationError("Password must contain number."))
        if not password or " " in password:
            self.add_error("password", ValidationError("Password contains empty spaces."))


class JoinPublicChatForm(forms.Form):
    chat_id = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Chat ID'}))

    def clean(self):
        clean_data = super().clean()
        url_id = clean_data.get("chat_id")
        room = models.ChatRoomPublic.objects.filter(url_id=url_id)
        if not room.exists():
            self.add_error("chat_id", ValidationError("Chat ID not found."))
        elif room[0].state != 1:
            self.add_error("chat_id", ValidationError("Chat Room has been closed."))


class JoinPrivateChatForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Username'}))

    def clean(self):
        clean_data = super().clean()
        if not models.User.objects.filter(username=clean_data.get("username")).exists():
            self.add_error("username", ValidationError("Username not found."))

class ChatInputForm(forms.Form):
    text = forms.CharField(max_length=255, label=False, widget=forms.TextInput(attrs={'placeholder':'Message here'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ""

class CreatePublicRoomForm(forms.Form): 
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Room Name'}))