from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.ChatRoomPublic)
admin.site.register(models.ChatRoomPrivat)
admin.site.register(models.TextMessagePublic)
admin.site.register(models.TextMessagePrivat)