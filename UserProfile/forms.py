from django import forms
from .models import friendRequest

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
