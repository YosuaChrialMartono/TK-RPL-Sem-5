from django.urls import path
from .views import show_all_kelas, mentee_home, join_kelas

app_name = 'mentee'

urlpatterns = [
    path('', mentee_home, name='mentee-home'),
    path('kelas-tersedia/', show_all_kelas, name='show_all_kelas'),
    path('join/', join_kelas, name='join_kelas'),
]
