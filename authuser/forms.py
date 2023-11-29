from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Mentor, Mentee


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'bio')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if user.role == '1':
                Mentor.objects.create(user=user)
            elif user.role == '2':
                Mentee.objects.create(user=user)
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput())
