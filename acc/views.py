from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView


class UserSignInView(LoginView):
    template_name = 'acc/login.html'
    redirect_authenticated_user = True


class UserSignOutView(LogoutView):
    pass


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
            return redirect('codeload:tasklist')
        else:
            error = 'Something went wrong...'
    registration_form = UserCreationForm()
    return render(request, 'acc/registration.html', {
        'form': registration_form,
        'error': error
    })
