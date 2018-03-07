from django.shortcuts import render
from django.contrib.auth import authentificate, login
from django.url import HttpRedirectResponse


# Create your views here.


def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authentificate(username, password)
        if not user is None:
            login(username, password)
            return HttpRedirectResponse(reverse('cle_django:index'))
        else:
            return HttpRedirectResponse(reverse('acc:login', args = (
                error = 'Invalid login!'
            )))


def logout(request):
    

def register(request):
        