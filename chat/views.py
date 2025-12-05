from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models

# Create your views here.

def home_redirect(request):
    return redirect('chat:home')

def home(request):
    return HttpResponse("this is the home page")

def test_create_user(request):
    missing = []
    username = request.GET.get('username')
    if not username:
        missing.append('username')
    email = request.GET.get('email')
    if not email:
        missing.append('email')
    password = request.GET.get('password')
    if not password:
        missing.append('password')
    if missing:
        return HttpResponse(f"{missing} parameters missing")

    models.User.objects.create(username=username,email=email,password=password)

    return HttpResponse(f"user {username} has been created")

def test_create_pubchat(request):
    try:
        last_id = models.ChatRoomPublic.objects.last().id
    except:
        last_id = 0
    last_id = str(last_id + 1) 
    url_id = "0"*(10-len(last_id)) + last_id
    models.ChatRoomPublic.objects.create(url_id=url_id)

    return HttpResponse(f"new public room with id {url_id} has been created.")

def test_add_pubuser(request):
    models.ChatRoomPublic.objects.filter(url_id='0000000001')[0].user.add(models)

def text_create_pubtext(request):
    pass

def test_create_privchat(request):
    pass

def test_create_privtext(request):
    pass

def test(request):
    new_user = models.User.objects.create(username="tim",email="time@mail.fr",password="123")
    try:
        last_id = models.ChatRoomPublic.objects.last().id
    except:
        last_id = 0
    last_id = str(last_id + 1) 
    url_id = "0"*(10-len(last_id)) + last_id
    new_pubchat = models.ChatRoomPublic.objects.create(url_id=url_id)

    new_pubchat.user.add(new_user)

    new_user2 = models.User.objects.create(username="tom",email="tome@mail.fr",password="123")
    new_privchat = models.ChatRoomPrivat.objects.create(url_id="10-11", user_1=new_user, user_2=new_user2)

    return HttpResponse("test")

