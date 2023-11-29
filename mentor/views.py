from django.shortcuts import render
from django.http import HttpResponse
from .decorators import mentor_required
from django.db import DatabaseError
from .forms import KelasForm
from .models import Kelas
# Create your views here.

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