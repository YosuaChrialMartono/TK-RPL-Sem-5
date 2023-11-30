from django.urls import path
from . import views

app_name = 'mentor'

urlpatterns = [
    path('', views.index, name='index'),
    path('create-kelas/', views.create_kelas, name='create_kelas'),
    path('my-kelas/', views.my_kelas, name='my_kelas'),
    ]