from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_content']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating harus berada di antara 1 dan 5.")
        return rating

    def clean_review_content(self):
        review_content = self.cleaned_data.get('review_content')
        if not review_content.strip():
            raise forms.ValidationError("Isi ulasan tidak boleh kosong.")
        return review_content