from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    #password = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.username

# class Guest(models.Model):
#     guestname = models.CharField(max_length=255, unique=True, default="Guest")

class ChatRoomPublic(models.Model):
    STATES = (
        (0, "closed"),
        (1, "active"),
    )
    user = models.ManyToManyField(User, related_name='public_users')
#   guest = models.ManyToManyField(Guest, blank=True, related_name='public_guests')
    url_id = models.CharField(max_length=10, unique=True)        # 0s + row id (0s till the total amount of characters is 10 eg '0000000012' for id 12)
    state = models.SmallIntegerField(choices=STATES, default=1)

    def __str__(self):
        return self.url_id
    
class TextMessagePublic(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)
    chat_room = models.ForeignKey(ChatRoomPublic, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True, related_name='public_text_user')

    def __str__(self):
        return f"{str(self.time_stamp)}: {str(self.content)}"
    
    def clean(self):
        if not self.chat_room.user.filter(id=self.user.id).exists():
            raise ValidationError('User not member of chatroom')


class ChatRoomPrivat(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='privat_user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='privat_user_2')
    url_id = models.CharField(max_length=50, unique=True)  # '(user id)-(other user id)' (the first id is the lower of the 2)

    def __str__(self):
        return self.url_id

    def clean(self):
        if self.user_1.id == self.user_2.id:
            raise ValidationError("Users have to be different.")

class TextMessagePrivat(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)
    chat_room = models.ForeignKey(ChatRoomPrivat, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True, related_name='privat_text_user')

    def __str__(self):
        return f"{str(self.time_stamp)}: {str(self.content)}"
    
    def clean(self):
        user_id = self.user.id
        if not (user_id == self.chat_room.user_1.id or user_id == self.chat_room.user_2.id):
            raise ValidationError('User not member of privat chat.')
    
    


