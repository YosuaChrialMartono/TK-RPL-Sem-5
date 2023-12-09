from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, LoginForm
from mentee.models import Mentee
from mentor.models import Mentor

User = get_user_model()

def index(request):
    return render(request, 'index.html')

from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Akun berhasil dibuat!")
            response = JsonResponse({'success': True})
            return response
        else:
            print(form.errors)
            errors = {field: form.errors[field][0] for field in form.errors}
            response = JsonResponse({'success': False, 'errors': errors})
            return response
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form, 'errors': form.errors})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Berhasil login!")
                response_data = {'success': True}
            else:
                response_data = {'success': False, 'errors': {'login': 'Invalid login credentials'}}
        else:
            errors = {field: form.errors[field][0] for field in form.errors}
            response_data = {'success': False, 'errors': errors}

        return JsonResponse(response_data)

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "Berhasil logout!")
    return redirect('authuser:login')
