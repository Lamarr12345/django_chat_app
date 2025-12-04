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
    models.Guest.objects.create(guestname=username)

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

