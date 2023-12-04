from django.shortcuts import render, redirect
from django.http import HttpResponse
from .decorators import mentor_required
from django.db import DatabaseError
from kelas.forms import KelasForm
from kelas.models import Kelas
import kelas.views as kelas_func

@mentor_required(login_url='authuser:login')
def index(request):
    return HttpResponse("Hello, world. You're at the mentor index.")

@mentor_required(login_url='authuser:login')
def create_kelas(request):
    if request.method == 'POST':
        form = KelasForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                form.save()
                # Redirect after successful save
                return redirect('mentor:my_kelas')
            except DatabaseError:
                form.add_error(None, 'Failed to save data to the database.')
    else:
        form = KelasForm()

    return render(request, 'buat-kelas.html', {'form': form})

@mentor_required(login_url='authuser:login')
def my_kelas(request):
    kelas = Kelas.objects.filter(mentor_kelas=request.user.mentor)
    context = {
        'kelas_saya': kelas
    }
    return render(request, 'my-kelas.html', context)



@mentor_required(login_url='authuser:login')
def update_status_pembayaran(request, idKelas, idForm):
    status_konfirmasi = request.GET.get('status', '')
    status_konfirmasi = str.lower(status_konfirmasi)
    if status_konfirmasi not in ['tolak', 'terima']:
        return HttpResponse(status=400, content=f"Parameter status tidak valid")
    
    forms = kelas_func.filter_form_by_kelas(idKelas)
    if forms is None:
        return HttpResponse(status=400, content=f'Kelas dengan id {idKelas} tidak ditemukan')
    
    form = [value for value in forms if value.id == int(idForm)]
    if len(form) == 0:
        return HttpResponse(status=400, content=f'Form dengan id {idForm} tidak ditemukan')
    
    form = form[0]
    mentee = form.pendaftar
    kelas = form.kelas
    
    response = kelas_func.update_status(request, form, mentee, kelas, status_konfirmasi)
    
    return response
    