from django.shortcuts import render
from authuser.models import User
from .models import friendRequest
from PIL import Image

def view_profile(request, username):
    is_authenticated = False
    is_same_person = False
    if request.user.is_authenticated:
        is_authenticated = True
        if request.user.username == username:
            is_same_person = True
            user_profile = User.objects.get(username = username)

    user_profile = User.objects.get(username = username)
    user_profile_email = user_profile.get_email()
    user_profile_role = user_profile.get_role_display() 
    user_profile_friend_count = friendRequest.objects.filter(user = user_profile.get_id(), friend = user_profile.get_id(), accepted_status = True).count()
    user_profile_bio = user_profile.get_bio()
    user_profile_profile_picture = user_profile.profile_picture

    context = {
        'username': username,
        'email': user_profile_email,
        'role': user_profile_role,
        'friend_count': user_profile_friend_count,
        'bio': user_profile_bio,
        'profile_picture' : user_profile_profile_picture,
        'is_same_person': is_same_person,
        'is_authenticated': is_authenticated,
    }

    return render(request, 'profile.html', context)
