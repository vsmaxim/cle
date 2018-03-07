from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views

app = 'acc'
urlpatterns = [
    path('', views.auth, name='login'),
    path('logout/', views.leave, name='logout'),
    path('register/', views.register, name = 'register'),
]