from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import ValidationError
from .validators.helper import is_private_member, is_public_member
from datetime import datetime
from django.db.models import Q
from . import models
from . import forms
from django.utils import timezone
from django.db.models import Count

# Create your views here.

def home_redirect(request):
    return redirect('chat:home')

def home(request):
    if request.user.is_authenticated:
        return redirect('chat:user-home', user_id = request.user.id)
    return render(request, "home.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('chat:user-home', user_id = user.id)
        form = forms.LoginForm(request.POST)
        return render(request, "login.html", {"form": form})
    else:
        form = forms.LoginForm()
        return render(request, "login.html", {"form": form})

def logout(request):
    auth_logout(request)
    return render(request, "logout.html")


def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            models.User.objects.create_user(username=username, email=email, password=password)
                  
            return redirect('chat:home')

        return render(request, "signup.html", {"form": form})
    else:
        form = forms.SignupForm()
        return render(request, "signup.html", {"form": form})


def user_home(request, user_id):
    if request.user.is_authenticated and request.user.id == user_id:
        form_public = None
        form_private = None
        form_type = request.POST.get("form-type")
        if form_type == "public-chat-rooms":
            return redirect("chat:user-public-chats", user_id = request.user.id)

        if form_type == "join-public-chat-room":
            form_public = forms.JoinPublicChatForm(request.POST)
            if form_public.is_valid():
                url_id = request.POST.get("chat_id")
                if not is_public_member(request.user, url_id):
                    models.ChatRoomPublic.objects.filter(url_id=url_id)[0].user.add(request.user)
                return redirect("chat:user-public-chat-room", user_id, url_id)

        if form_type == "private-chat-rooms":
            return redirect("chat:user-private-chats", user_id = request.user.id)

        if form_type == "join-private-chat-room":
            form_private = forms.JoinPrivateChatForm(request.POST)
            if request.user.username == request.POST.get("username"):
                form_private.add_error("username", ValidationError("Username can't be your own."))
            if form_private.is_valid():
                me = request.user
                other = models.User.objects.get(username=request.POST.get("username"))
                if int(me.id) < int(other.id):
                    user_1 = me
                    user_2 = other
                else:
                    user_1 = other
                    user_2 = me
                url_id = f"{user_1.id}-{user_2.id}"
                
                models.ChatRoomPrivat.objects.get_or_create(user_1=user_1,
                                                            user_2=user_2,
                                                            url_id=url_id)
                
                return redirect("chat:user-private-chat-room", user_id, url_id)
                
        if not form_public:
            form_public = forms.JoinPublicChatForm()
        if not form_private:
            form_private = forms.JoinPrivateChatForm()

        context = {"username" : request.user.username, "form_public":form_public, "form_private": form_private}
        return render(request, "user_home.html", context=context)
    
    else:
        return render(request, "no_access.html")
    


def user_public_chats(request, user_id):
    if request.user.is_authenticated and request.user.id == user_id:
        if request.GET.get("order") in ["url_id", "name", "owner", "-total_members"]:
            chat_list_order = request.GET.get("order")
        else:
            chat_list_order = "-last_updated"

        create_form = forms.CreatePublicRoomForm(request.POST or None)
        public_rooms = models.ChatRoomPublic.objects.filter(state=1).annotate(total_members=Count("user")).order_by(chat_list_order)
        user_public_rooms = models.ChatRoomPublic.objects.filter(owner=request.user, state=1).annotate(total_members=Count("user"))

        if request.method == 'POST':
            if not len(models.ChatRoomPublic.objects.filter(owner=request.user, state=1)) < 3:
                create_form.add_error("name", ValidationError("User has too many open rooms."))
            if create_form.is_valid():
                name = request.POST.get("name")
                all_public_rooms = models.ChatRoomPublic.objects.all()
                if all_public_rooms:
                    next_id = int(all_public_rooms.last().id) + 1
                else:
                    next_id = 1
                next_id = str(next_id)
                url_id = "0"*(8-len(next_id)) + next_id
                created_room = models.ChatRoomPublic.objects.create(name=name, url_id=url_id, owner=request.user)
                created_room.user.add(request.user)
                create_form = forms.CreatePublicRoomForm()

        context = {"user": request.user, "create_form": create_form, "public_rooms": public_rooms, "user_public_rooms": user_public_rooms}
        return render(request, "user_public_chats.html", context=context)
    else:
        return render(request, "no_access.html")


def user_public_chat_room(request, user_id, url_id):
    if request.user.is_authenticated and request.user.id == user_id and is_public_member(request.user, url_id):
        room = models.ChatRoomPublic.objects.get(url_id=url_id)
        
        if request.POST.get("text"):
            models.TextMessagePublic.objects.create(content=request.POST.get("text"),
                                                                chat_room = room,
                                                                user = request.user)
            room.last_updated = timezone.now()
            room.save()

        chat_msgs = models.TextMessagePublic.objects.filter(chat_room=room).order_by('-time_stamp')
        chat_msgs.query.set_limits(high=20)

        form = forms.ChatInputForm()
        context = {"room":room, "chat_msgs":chat_msgs, "form": form}
        return render(request, "user_public_chat_room.html",context=context)
    else:
        return render(request, "no_access.html")


def user_private_chats(request, user_id):
    if request.user.is_authenticated and request.user.id == user_id:
        rooms = models.ChatRoomPrivat.objects.filter(Q(user_1 = request.user) | Q(user_2 = request.user)).order_by("-last_updated")

        room_data = []
        for room in rooms:
            if room.user_1 == request.user:
                room_data.append({"room": room, "other_user":room.user_2})
            else:
                room_data.append({"room": room, "other_user":room.user_1})

        return render(request, "user_private_chats.html", {"room_data" : room_data, "user" : request.user})
    else:
        return render(request, "no_access.html")


def user_private_chat_room(request, user_id, url_id):
    if request.user.is_authenticated and request.user.id == user_id and is_private_member(request.user, url_id):
        room = models.ChatRoomPrivat.objects.get(url_id=url_id)
        
        if request.POST.get("text"):
            models.TextMessagePrivat.objects.create(content=request.POST.get("text"),
                                                                chat_room = room,
                                                                user = request.user)
            room.last_updated = timezone.now()
            room.save()

        chat_msgs = models.TextMessagePrivat.objects.filter(chat_room=room).order_by('-time_stamp')
        chat_msgs.query.set_limits(high=20)

        form = forms.ChatInputForm()
        context = {"user_1": room.user_1.username, "user_2": room.user_2.username, "chat_msgs":chat_msgs, "form": form, "user": request.user}
        return render(request, "user_private_chat_room.html",context=context)
    else:
        return render(request, "no_access.html")

# helper urls

def user_private_chat_room_join(request, user_id, url_id):
    if request.user.is_authenticated and request.user.id == user_id:
  
        return redirect("chat:user-private-chat-room", user_id, url_id)
    else:
        return render(request, "no_access.html")
    

def user_public_chat_room_join(request, user_id, url_id):
    if request.user.is_authenticated and request.user.id == user_id:

        if not is_public_member(request.user, url_id):
            models.ChatRoomPublic.objects.filter(url_id=url_id)[0].user.add(request.user)
  
        return redirect("chat:user-public-chat-room", user_id, url_id)
    else:
        return render(request, "no_access.html")


def user_public_chat_room_close(request, user_id, url_id):
    if request.user.is_authenticated and request.user.id == user_id:

        rooms = models.ChatRoomPublic.objects.filter(url_id=url_id, owner=request.user)
        if rooms:
            rooms[0].state = 0
            rooms[0].save()
  
        return redirect("chat:user-public-chats", user_id)
    else:
        return render(request, "no_access.html")
     


