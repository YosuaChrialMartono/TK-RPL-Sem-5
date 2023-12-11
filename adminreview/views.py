from django.shortcuts import render, redirect, get_object_or_404
from adminreview.models import Materi
from adminreview.forms import TinjauMateriForm
from django.contrib import messages
from kelas.models import Kelas
from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    """
    Decorator for views that checks if the user is an admin (superuser).
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='authuser:login',  
    )
    return actual_decorator(view_func)

@admin_required
def tinjau_kelas(request, kelas_id):
    list_kelas = Kelas.objects.filter(pk=kelas_id)

    return render(request, 'tinjau_kelas.html', {'list_kelas': list_kelas})

@admin_required
def pengelolaan_materi(request):
    list_kelas = Kelas.objects.all()

    return render(request, 'pengelolaan_materi.html', {'list_kelas': list_kelas})

@admin_required
def tinjau_materi(request, kelas_id):
    kelas = get_object_or_404(Kelas, id=kelas_id)
    materi_list = Materi.objects.filter(kelas=kelas)

    return render(request, 'tinjau_materi.html', {'kelas': kelas, 'materi_list': materi_list})

@admin_required
def persetujuan_materi(request, materi_id):
    materi = get_object_or_404(Materi, id=materi_id)

    if request.method == 'POST':
        form = TinjauMateriForm(request.POST, instance=materi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success to save feedback.')
            return redirect('adminreview:tinjau_materi', kelas_id=materi.kelas.id)
    else:
        form = TinjauMateriForm(instance=materi)

    return render(request, 'persetujuan_materi.html', {'materi': materi, 'form': form})