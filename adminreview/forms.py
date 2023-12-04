from django import forms
from django.core.exceptions import ValidationError
from adminreview.models import Materi

def validate_non_empty(value):
    if value.strip() == '':
        raise ValidationError('Feedback cannot be empty.')
    
class TinjauMateriForm(forms.ModelForm):
    class Meta:
        model = Materi
        fields = ['status_persetujuan', 'feedback']

    STATUS_CHOICES = [
        ('Menunggu Persetujuan', 'Menunggu Persetujuan'),
        ('Disetujui', 'Disetujui'),
    ]

    status_persetujuan = forms.ChoiceField(choices=STATUS_CHOICES, label='Status Persetujuan')
    feedback = forms.CharField(validators=[validate_non_empty], widget=forms.Textarea(attrs={'rows': 3}))
