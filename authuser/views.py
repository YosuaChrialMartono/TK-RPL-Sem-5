from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, LoginForm
from .models import Mentor, Mentee

User = get_user_model()

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('authuser:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    form = LoginForm()
    error_message = None 

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('authuser:index')  # Ganti nanti
        else:
            error_message = 'Username atau password salah'
            messages.error(request, error_message)

    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def logout_user(request):
    logout(request)
    return redirect('authuser:login')
