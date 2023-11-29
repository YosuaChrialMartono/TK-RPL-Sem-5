from django.urls import path
from authuser.models import User
from .views import view_profile

app_name = 'UserProfile'

urlpatterns = [
    path('<str:username>', view_profile, name='view_profile'),
]
