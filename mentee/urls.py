from django.urls import path
from .views import show_all_kelas, mentee_home, join_kelas, add_bukti_pembayaran,\
    show_form_pendaftaran, get_form_by_id

app_name = 'mentee'

urlpatterns = [
    path('', mentee_home, name='mentee-home'),
    path('kelas-tersedia/', show_all_kelas, name='show_all_kelas'),
    path('join/', join_kelas, name='join_kelas'),
    path('form-pendaftaran/', show_form_pendaftaran, name='form_pendaftaran'),
    path('form-pendaftaran/<str:idForm>', get_form_by_id, name='form_by_id'),
    path('form-pendaftaran/<str:idForm>/add-bukti', add_bukti_pembayaran, name='add_bukti'),
]
