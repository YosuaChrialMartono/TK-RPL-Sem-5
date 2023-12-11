from django.shortcuts import render, redirect
from review.models import Review
from kelas.models import Kelas
from mentee.models import Mentee
from review.forms import ReviewForm
from django.contrib import messages
from review.decorators import mentee_required

@mentee_required(login_url='authuser:login')
def classes_followed(request):
    mentee_id = request.user.id
    kelas_diikuti = Kelas.objects.filter(mentee_kelas=mentee_id)
    return render(request, 'review_kelas.html', {'kelas_diikuti': kelas_diikuti})

@mentee_required(login_url='authuser:login')
def review_kelas(request):
    mentee = request.user.id
    reviews = Review.objects.filter(reviewer_id=mentee)

    # Ambil semua kelas yang pernah diikuti oleh mentee
    kelas_diikuti = Kelas.objects.filter(mentee_kelas=mentee)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            kelas_id = request.POST.get('kelas_id')
            review = form.save(commit=False)
            review.reviewer = Mentee.objects.get(pk=mentee)
            review.reviewed_kelas = Kelas.objects.get(pk=kelas_id)
            review.save()
            messages.success(request, 'Ulasan berhasil disimpan.')
            return render(request, 'review_kelas.html', {'reviews': reviews, 'form': form, 'kelas_diikuti': kelas_diikuti})
        else:
            messages.error(request, 'Mohon isi semua bidang dengan benar.')
    else:
        form = ReviewForm()

    return render(request, 'review_kelas.html', {'reviews': reviews, 'form': form, 'kelas_diikuti': kelas_diikuti})