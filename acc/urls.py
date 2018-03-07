from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views

app = 'acc'
urlpatterns = [
    path('login/', views.login, mame='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name = 'register'),
]