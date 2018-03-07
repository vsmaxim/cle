from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views

app = 'acc'
urlpatterns = [
    path('', views.index, name='auth_page'),
    path('<str:error>', views.index, name='auth_failed'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name = 'register'),
]