from django.db import models

# Create your models here.

class RoomID(models.Model):
    room_id = models.CharField(max_length=10, unique=True)
    state = models.CharField(max_length=255)

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, null=False)

class ChatRoom(models.Model):
    users = models.ManyToManyField(User, related_name='participants')
    room_id = models.OneToOneField(RoomID, on_delete=models.CASCADE)

class TextMessage(models.Model):
    content = models.CharField(max_length=500)
    time_stamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='users')
    chat = models.OneToOneField(ChatRoom, on_delete=models.CASCADE)

class PrivatChatLog(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user2')

class Guest(models.Model):
    guestname = models.CharField(max_length=255, unique=True, default="Guest")
