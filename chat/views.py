from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models

# Create your views here.

def home_redirect(request):
    return redirect('chat:home')

def home(request):
    context = {
    }
    return render(request, "home.html", context=context)


def login(request):
    context = {
    }
    return render(request, "login.html", context=context)


def signup(request):
    context = {
    }
    return render(request, "signup.html", context=context)


def user_home(request, user_id):
    username = "john"
    context = {
        "username" : username
    }
    return render(request, "user_home.html", context=context)


def user_public_chats(request, user_id):
    context = {
    }
    return render(request, "user_public_chats.html", context=context)


def user_public_chat_room(request, user_id, url_id):
    context = {
    }
    return render(request, "user_public_chat_room.html", context=context)


def user_private_chats(request, user_id):
    context = {
    }
    return render(request, "user_private_chats.html", context=context)


def user_private_chat_room(request, user_id, url_id):
    context = {
    }
    return render(request, "user_private_chat_room.html", context=context)



