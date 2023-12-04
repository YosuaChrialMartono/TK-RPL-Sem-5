from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render

from authuser.models import User
from mentee.models import Mentee
from .decorators import mentee_required
import kelas.views as kelas_func

@mentee_required(login_url='authuser:login')
def mentee_home(request):
    return render(request, 'mentee-home.html')

@mentee_required(login_url='authuser:login')
def show_all_kelas(request):
    classes = kelas_func.all_kelas()

    return render(request, 'show_all_kelas.html', {'semua_kelas': classes})

@mentee_required(login_url='authuser:login')
def join_kelas(request):
    judul_kelas = request.GET.get('kelas', '')
    if judul_kelas == '':
        return HttpResponseBadRequest('Tidak ada parameter nama kelas yang ingin diikuti')
    
    kelas = kelas_func.filter_kelas_by_judul(judul=judul_kelas)
    if kelas is None:
        return HttpResponseBadRequest('Kelas yang ingin diikuti tidak ada')
    
    try:
        mentee = Mentee.objects.get(user=request.user)
    except Mentee.DoesNotExist:
        return HttpResponseNotFound('Mentee tidak ditemukan')

    response = kelas_func.join_kelas(request, mentee, kelas)

    return response