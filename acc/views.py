from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Create your views here.

def auth(request):
    error = None
    if (request.method == 'POST'):
        login_form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if not user is None:
            login(request, user)
            return redirect('codeload:task', pk = 1)
        else:
            error = 'Login incorrect'
    login_form = AuthenticationForm()
    
    return render(request, 'acc/login.html', {
            'form' : login_form,
            'error': error
    })

def leave(request):
    logout(request)
    # Change it
    return redirect('http://yandex.ru')

def register(request):
    error = None
    if (request.method == 'POST'):
        registration_form = UserCreationForm(request.POST)
        if (registration_form.is_valid()):
            registration_form.save()
            username = registration_form.cleaned_data.get('username')
            password = registration_form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            login(request, user)
            return redirect('codeload:task', pk = 1)
        else:
            error = 'Something went wrong...'
    registration_form = UserCreationForm()
    return render(request, 'acc/registration.html', {
        'form': registration_form,
        'error': error
    })
