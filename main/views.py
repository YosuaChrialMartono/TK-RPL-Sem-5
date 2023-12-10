from django.shortcuts import render
from kelas.models import Kelas

def main_page(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'kelas' : Kelas.objects.all(),
            'is_mentor' : False,
            'is_mentee' : False,
        }
        if request.user.role == '1':
            context['is_mentor'] = True
            context['kelas_saya'] = Kelas.objects.filter(mentor_kelas=request.user.id)
            return render(request, 'main-page.html', context)
        elif request.user.role == '2':
            context['kelas_saya'] = Kelas.objects.filter(mentee_kelas=request.user.id)
            context['is_mentee'] = True
            return render(request, 'main-page.html', context)
        return render(request, 'main-page.html', context)
    else:
        return render(request, 'main-page.html')