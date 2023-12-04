from django.urls import path
from .views import get_all_kelas, get_form_by_kelas, get_form_by_id

app_name = 'kelas'

urlpatterns = [
    path('', get_all_kelas, name='all_kelas'),
    path('<str:idKelas>/form', get_form_by_kelas, name='all_form'),
    path('<str:idKelas>/form/<str:idForm>', get_form_by_id, name='get-form-id'),
    # path('<str:idKelas>/form/<str:idForm>/update', update_status_pembayaran, name='update_status_pembayaran')
]