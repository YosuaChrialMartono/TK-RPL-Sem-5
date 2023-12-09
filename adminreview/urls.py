from django.urls import path
from adminreview.views import pengelolaan_materi, tinjau_materi

app_name = 'adminreview'

urlpatterns = [
    path('pengelolaan_materi/', pengelolaan_materi, name='pengelolaan_materi'),
    path('tinjau_materi/<int:materi_id>/', tinjau_materi, name='tinjau_materi'),
]