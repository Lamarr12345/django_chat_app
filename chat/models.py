import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        """Override save to always call full_clean()"""
        self.full_clean()
        super().save(*args, **kwargs)

# class Guest(models.Model):
#     guestname = models.CharField(max_length=255, unique=True, default="Guest")

class ChatRoomPublic(models.Model):
    STATES = (
        (0, "closed"),
        (1, "active"),
    )
    name = models.CharField(max_length=255)
    user = models.ManyToManyField(User, blank=True, related_name='public_users')
#   guest = models.ManyToManyField(Guest, blank=True, related_name='public_guests')
    url_id = models.CharField(max_length=10, unique=True)        # 0s + row id (0s till the total amount of characters is 10 eg '0000000012' for id 12)
    state = models.SmallIntegerField(choices=STATES, default=1)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='public_chat_owner')
    last_updated = models.DateTimeField(null=False, default=timezone.now)

    def __str__(self):
        return f"{self.url_id}: {self.name}"
    
    def save(self, *args, **kwargs):
        """Override save to always call full_clean()"""
        self.full_clean()
        super().save(*args, **kwargs)
    
class TextMessagePublic(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)
    chat_room = models.ForeignKey(ChatRoomPublic, on_delete=models.CASCADE, db_index=True, related_name='public_text_chat')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True, related_name='public_text_user')

    def __str__(self):
        return f"{str(self.time_stamp)}: {str(self.content)}"
    
    def clean(self):
        if not self.chat_room.user.filter(pk=self.user.id).exists():
            raise ValidationError('User not member of chatroom')

    def save(self, *args, **kwargs):
        """Override save to always call full_clean()"""
        self.full_clean()
        super().save(*args, **kwargs)

class ChatRoomPrivat(models.Model):
    STATES = (
        (0, "closed"),
        (1, "active"),
    )
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='privat_user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='privat_user_2')
    url_id = models.CharField(max_length=50, unique=True)  # '(user id)-(other user id)' (the first id is the lower of the 2)
    state = models.SmallIntegerField(choices=STATES, default=1)
    last_updated = models.DateTimeField(null=False, default=timezone.now)

    def __str__(self):
        return self.url_id

    def clean(self):
        if self.user_1.id == self.user_2.id:
            raise ValidationError("Users have to be different.")
        
    def save(self, *args, **kwargs):
        """Override save to always call full_clean()"""
        self.full_clean()
        super().save(*args, **kwargs)

class TextMessagePrivat(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)
    chat_room = models.ForeignKey(ChatRoomPrivat, on_delete=models.CASCADE, db_index=True, related_name='privat_text_chat')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True, related_name='privat_text_user')

    def __str__(self):
        return f"{str(self.time_stamp)}: {str(self.content)}"
    
    def clean(self):
        user_id = self.user.id
        if not (user_id == self.chat_room.user_1.id or user_id == self.chat_room.user_2.id):
            raise ValidationError('User not member of privat chat.')
    
    def save(self, *args, **kwargs):
        """Override save to always call full_clean()"""
        self.full_clean()
        super().save(*args, **kwargs)


