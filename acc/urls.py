from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views

app_name = 'acc'
urlpatterns = [
    path('', views.UserSignInView.as_view(), name='login'),
    path('logout/', views.UserSignOutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]