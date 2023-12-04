from django.urls import path
from review.views import review_kelas

app_name = 'review'

urlpatterns = [
    path('review_kelas/', review_kelas, name='review_kelas'),
]