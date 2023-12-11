from django.urls import path
from . import views
from kelas.views import get_form_by_kelas, get_form_by_id

app_name = 'mentor'

urlpatterns = [
    path('', views.index, name='index'),
    path('create-kelas/', views.create_kelas, name='create_kelas'),
    path('my-kelas/', views.my_kelas, name='my_kelas'),
    path('my-kelas/<str:idKelas>/bukti-pembayaran', views.show_bukti_pembayaran, name='bukti_pembayaran'),
    path('my-kelas/<str:idKelas>/form', get_form_by_kelas, name='all_form_kelas'),
    path('my-kelas/<str:idKelas>/form/<str:idForm>', get_form_by_id, name='get_form_id'),
    path('my-kelas/<str:idKelas>/form/<str:idForm>/update', views.update_status_pembayaran, name='update_status_pembayaran'),
]