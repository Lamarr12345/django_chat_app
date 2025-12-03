from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def home_redirect(request):
    return redirect('chat:home')

def home(request):
    return HttpResponse("this is the home page")
