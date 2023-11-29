from django.shortcuts import render
from django.http import HttpResponse
from .decorators import mentor_required

# Create your views here.

@mentor_required(login_url='authuser:login')
def index(request):
    return HttpResponse("Hello, world. You're at the mentor index.")