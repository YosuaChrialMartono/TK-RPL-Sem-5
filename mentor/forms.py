from django import forms
from django.core.exceptions import ValidationError
from .models import Kelas, Mentor

class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = ['judul_kelas', 'tanggal_kelas', 'harga_kelas', 'mentor_kelas']

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

    def clean_mentor_kelas(self):
        mentor_kelas = self.cleaned_data.get('mentor_kelas')
        if not mentor_kelas:
            raise ValidationError('Mentor kelas is required.')
        return mentor_kelas