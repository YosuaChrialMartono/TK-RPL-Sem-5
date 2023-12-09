from django.shortcuts import render, redirect, get_object_or_404
from adminreview.models import Materi
from adminreview.forms import TinjauMateriForm
from django.contrib import messages
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
def pengelolaan_materi(request):
    materi_list = Materi.objects.all()

    return render(request, 'pengelolaan_materi.html', {'materi_list': materi_list})

@admin_required
def tinjau_materi(request, materi_id):
    materi = get_object_or_404(Materi, id=materi_id)

    if request.method == 'POST':
        form = TinjauMateriForm(request.POST, instance=materi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback dan status materi berhasil diperbarui.')
            return redirect('adminreview:pengelolaan_materi')
        else:
            messages.error(request, 'Mohon isi semua bidang dengan benar.')
    else:
        form = TinjauMateriForm(instance=materi)

    return render(request, 'tinjau_materi.html', {'form': form, 'materi': materi})
