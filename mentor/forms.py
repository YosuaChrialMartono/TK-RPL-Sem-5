from django import forms
from django.core.exceptions import ValidationError
from .models import Kelas, Mentor
import datetime

class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = ['judul_kelas', 'tanggal_kelas', 'harga_kelas']
        widgets = {
            'tanggal_kelas': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(KelasForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        kelas = super(KelasForm, self).save(commit=False)
        if self.user and isinstance(self.user.mentor, Mentor):
            kelas.mentor_kelas = self.user.mentor
        if commit:
            kelas.save()
        return kelas
    
    def clean(self):
        cleaned_data = super().clean()
        if self.user is None or not hasattr(self.user, 'mentor') or not isinstance(self.user.mentor, Mentor):
            raise ValidationError('The logged in user must be a mentor.')
        return cleaned_data

    def clean_judul_kelas(self):
        judul_kelas = self.cleaned_data.get('judul_kelas')
        if not judul_kelas:
            raise ValidationError('Judul kelas is required.')
        return judul_kelas

    def clean_tanggal_kelas(self):
        tanggal_kelas = self.cleaned_data.get('tanggal_kelas')
        if not tanggal_kelas:
            raise ValidationError('Tanggal kelas is required.')
        elif tanggal_kelas < datetime.date.today():
            raise ValidationError('Tanggal kelas cannot be in the past.')
        return tanggal_kelas

    def clean_harga_kelas(self):
        harga_kelas = self.cleaned_data.get('harga_kelas')
        if harga_kelas < 0:
            raise ValidationError('Harga kelas cannot be negative.')
        return harga_kelas