import os
from django.contrib.auth.forms import UserCreationForm
from django import forms
from PIL import Image
import time

from tk_rpl_django import settings
from .models import User
from mentee.models import Mentee
from mentor.models import Mentor

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'bio', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        profile_picture = self.cleaned_data.get('profile_picture')
        if commit:
            if profile_picture != '' and profile_picture is not None:
                filename = time.strftime("%Y%m%d-%H%M%S") + profile_picture.name 
                profile_picture_path = os.path.join(settings.MEDIA_ROOT, 'profile_pictures', filename)

                img = Image.open(profile_picture)
                
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                max_size = (300, 300)
                
                img.save(profile_picture_path, 'JPEG')
                user.save()
                if user.role == '1':
                    Mentor.objects.create(user=user)
                elif user.role == '2':
                    Mentee.objects.create(user=user)
            elif profile_picture == '' or profile_picture is None:
                user.save()
                if user.role == '1':
                    Mentor.objects.create(user=user)
                elif user.role == '2':
                    Mentee.objects.create(user=user)
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput())
