from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from . import forms

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

def logout(request):
    context = {
    }
    return render(request, "logout.html", context=context)


def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            models.User.objects.create(username=username, email=email, password=password)

            return redirect('chat:home')
        return redirect('chat:signup')
    else:
        form = forms.SignupForm()
        return render(request, "signup.html", {"form": form})


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

# # form funtions

# def create_user(request):
#     pass



