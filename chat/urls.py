from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path('', views.home_redirect, name='redirect-to-home'),
    path('home/', views.home, name='home'),
]
