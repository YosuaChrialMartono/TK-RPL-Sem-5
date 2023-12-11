from django.urls import path
from adminreview.views import pengelolaan_materi, tinjau_materi, tinjau_kelas, persetujuan_materi

app_name = 'adminreview'

urlpatterns = [
    path('', pengelolaan_materi, name='pengelolaan_materi'),
    path('tinjau_materi/<int:kelas_id>/', tinjau_materi, name='tinjau_materi'),
    path('persetujuan_materi/<int:materi_id>/', persetujuan_materi, name='persetujuan_materi'),
    path('tinjau_kelas/<int:kelas_id>/', tinjau_kelas, name='tinjau_kelas'),
]