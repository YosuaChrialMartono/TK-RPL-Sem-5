from django.shortcuts import render, redirect
from review.models import Review
from kelas.models import Kelas
from review.forms import ReviewForm
from django.contrib import messages
from review.decorators import mentee_required

@mentee_required(login_url='authuser:login')
def review_kelas(request):
    mentee = request.user.id
    reviews = Review.objects.filter(reviewer_id=mentee)
    
    # Ambil semua kelas yang pernah diikuti oleh mentee
    kelas_diikuti = Kelas.objects.filter(mentee_kelas=mentee)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.mentee = mentee
            review.save()
            messages.success(request, 'Ulasan berhasil disimpan.')
            return redirect('review_kelas')
        else:
            messages.error(request, 'Mohon isi semua bidang dengan benar.')
    else:
        form = ReviewForm()

    return render(request, 'review_kelas.html', 
                  {'reviews': reviews, 'form': form, 'kelas_diikuti': kelas_diikuti})