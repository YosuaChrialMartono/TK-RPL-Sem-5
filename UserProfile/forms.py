

from PIL import Image
from django import forms
from .models import friendRequest
from django.contrib.auth.forms import UserChangeForm
from authuser.models import User

class FriendRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), required=False)
    def save(self, commit=True):
        friend_request = friendRequest()
        friend_request.message = self.cleaned_data['message']
        friend_request.user = self.user
        friend_request.friend = self.friend
        if commit:
            return friend_request
        return None

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['bio']

