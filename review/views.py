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
    mentee = Mentee.objects.get(pk=request.user.id)
    reviews = Review.objects.filter(reviewer_id=mentee)
    kelas_diikuti = Kelas.objects.filter(mentee_kelas=mentee)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        kelas_id = request.POST.get('kelas_id')

        kelas = Kelas.objects.get(pk=kelas_id)
        has_reviewed = Review.objects.filter(reviewer=mentee, reviewed_kelas=kelas).exists()


        if has_reviewed:
            messages.error(request, 'You have already reviewed this class.')
            return render(request, 'review_kelas.html', {'kelas_diikuti': kelas_diikuti})
    
        review = Review(rating = rating, 
                        review_content = review,
                        reviewer = mentee,
                        reviewed_kelas = kelas)
        review.save()
        messages.success(request, 'Success to save review.')
        return render(request, 'review_kelas.html', {'reviews': reviews, 'kelas_diikuti': kelas_diikuti})
    else:
        form = ReviewForm()

    return render(request, 'review_kelas.html', {'reviews': reviews, 'kelas_diikuti': kelas_diikuti})