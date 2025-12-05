from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path('', views.home_redirect, name='redirect-to-home'),
    path('home/', views.home, name='home'),
    path('test_create_user/', views.test_create_user, name='test-create-user'),
    path('test_create_pubchat/', views.test_create_pubchat, name='test-create-pubchat'),
    path('test/', views.test, name='test-create-pubchat'),
]
