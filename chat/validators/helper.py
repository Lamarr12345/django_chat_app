from .. import models

def is_public_member(user, url_id):
    chats = models.ChatRoomPublic.objects.filter(url_id=url_id, state=1)
    if not chats:
        return False
    
    chat = chats[0]

    if not chat.user.filter(pk=user.id).exists():
        return False
    
    return True


def is_private_member(user, url_id):
    chats = models.ChatRoomPrivat.objects.filter(url_id=url_id)
    if not chats:
        return False
    
    chat = chats[0]

    if not (user == chat.user_1 or user == chat.user_2):
        return False
    
    return True