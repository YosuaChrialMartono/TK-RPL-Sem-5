from django.urls import path
from .views import get_all_kelas, get_kelas_by_mentor

app_name = 'kelas'

urlpatterns = [
    path('', get_all_kelas, name='all_kelas'),
    path('<str:username_mentor>', get_kelas_by_mentor, name='get_kelas_by_mentor'),
]