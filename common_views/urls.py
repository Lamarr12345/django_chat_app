from django.urls import path, reverse
from . import views

app_name = "common_views"
urlpatterns = [
    path('', views.home_redirect, name='home-redirect'),
]
