from django.urls import path
from authuser.models import User
from .views import view_profile, send_friend_request, accept_friend_request, reject_friend_request

app_name = 'UserProfile'

urlpatterns = [
    path('profile/<str:username>', view_profile, name='view_profile'),
    path('friend/<str:username>', send_friend_request, name='send_friend_request'),
    path('accept/<str:username>', accept_friend_request, name='accept_friend_request'),
    path('reject/<str:username>', reject_friend_request, name='reject_friend_request'),
]
