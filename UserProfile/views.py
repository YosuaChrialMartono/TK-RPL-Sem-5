import time

from PIL import Image
from django.shortcuts import redirect, render
from UserProfile.decorators import is_current_user, user_required, friend_request_recipient
from UserProfile.forms import FriendRequestForm, EditProfileForm
from authuser.models import User
from .models import friendRequest
from django.db import models
from django.contrib import messages


def check_friend_request_exists(user, friend):
    is_friend = friendRequest.objects.filter(
        (models.Q(user=user, friend=friend) | models.Q(user=friend, friend=user)),
        accepted_status=True
    ).exists()

    friend_request_exists = friendRequest.objects.filter(
        (models.Q(user=user, friend=friend) | models.Q(user=friend, friend=user)),
        accepted_status=False
    ).exists()

    return is_friend, friend_request_exists


def view_profile(request, username):
    user_profile = User.objects.get(username=username)
    is_authenticated = request.user.is_authenticated
    is_same_person = request.user.username == username if is_authenticated else False
    if is_authenticated:
        is_friend, friend_request_exists = check_friend_request_exists(request.user, user_profile)
    else:
        is_friend = False
        friend_request_exists = False

    form = None
    if is_authenticated and not is_same_person and not is_friend and not friend_request_exists:
        form = FriendRequestForm()

    friend_requests = None
    if is_same_person:
        friend_requests = friendRequest.objects.filter(friend=user_profile.get_id(), accepted_status=False)

    user_profile_role = user_profile.get_role_display()
    friend_count = friendRequest.objects.filter(user=user_profile.get_id(), accepted_status=True,
                                                is_rejected=False).count()
    friend_count = friend_count + friendRequest.objects.filter(friend=user_profile.get_id(), accepted_status=True,
                                                               is_rejected=False).count()

    profile_picture = user_profile.profile_picture
    print(profile_picture)
    if profile_picture is not None and profile_picture != '':
        profile_picture = profile_picture.url
        print(profile_picture)
    else:
        user_profile.profile_picture = None
        user_profile.save()

    context = {
        'username': username,
        'user_profile': user_profile,
        'profile_picture': profile_picture,
        'role': user_profile_role,
        'friend_count': friend_count,
        'is_same_person': is_same_person,
        'is_authenticated': is_authenticated,
        'is_friend': is_friend,
        'friend_request_exists': friend_request_exists,
        'friend_requests': friend_requests,
        'form': form
    }

    return render(request, 'profile.html', context)

@user_required(login_url='authuser:login')
@is_current_user(login_url='authuser:login')
def view_profile_edit(request, username):
    form = EditProfileForm()

    context = {
        'form': form,
        'username': username
    }

    return render(request, 'edit_profile_page.html', context)

@user_required(login_url='authuser:login')
@is_current_user(login_url='authuser:login')
def profile_edit(request, username):
    user_profile = User.objects.get(username=username)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile.bio = form.cleaned_data['bio']
            user_profile.save()
            return redirect('UserProfile:view_profile', username)


@user_required(login_url='authuser:login')
@friend_request_recipient(login_url='authuser:login')
def accept_friend_request(request, username):
    user_username = request.user.username
    user = User.objects.get(username=username)
    friend_request = friendRequest.objects.filter(friend=request.user, user=user, accepted_status=False)
    if friend_request is not None:
        request.user.accept_friend_request(friend_request)
    else:
        return redirect('UserProfile:view_profile', user_username)
    return redirect('UserProfile:view_profile', user_username)

@user_required(login_url='authuser:login')
@friend_request_recipient(login_url='authuser:login')
def reject_friend_request(request, username):
    user_username = request.user.username
    user = User.objects.get(username=username)
    friend_request = friendRequest.objects.filter(friend=request.user, user=user, accepted_status=False)
    if friend_request is not None:
        request.user.reject_friend_request(friend_request)
    else:
        return redirect('UserProfile:view_profile', user_username)
    return redirect('UserProfile:view_profile', user_username)

@user_required(login_url='authuser:login')
def send_friend_request(request, username):
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)
        if form.is_valid() and form is not None:
            current_user = request.user
            form.friend = User.objects.get(username=username)
            form.user = current_user
            if form.friend == current_user:
                return redirect('UserProfile:view_profile', username)
            is_friend, friend_request_exists = check_friend_request_exists(current_user, form.friend)
            if is_friend or friend_request_exists:
                return redirect('UserProfile:view_profile', username)
            friend_request = form.save(commit=True)
            friend_request.save()

            messages.success(request, f"Friend request sent to {form.friend.username} successfully!")

    else:
        form = FriendRequestForm()
    return redirect('UserProfile:view_profile', username)
