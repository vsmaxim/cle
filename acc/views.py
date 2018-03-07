from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.


def index(request, error = None):
    login_form = AuthenticationForm(request)
    return render(request, 'acc/login.html', {'form' : login_form, 'error' : error})

def login(request):
    if (request.method == 'POST'):
        login_form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if not user is None:
            login(username, password)
            redirect('codeload:task', pk = 1)
        else:
            return redirect('auth_failed', error = 'Login failed')


def logout(request):
    pass

def register(request):
    pass