from django.urls import path
from review.views import review_kelas, classes_followed

app_name = 'review'

urlpatterns = [
    path('', classes_followed, name='classes_followed'),
    path('review_kelas/', review_kelas, name='review_kelas'),
]