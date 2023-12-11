from django.shortcuts import render
from kelas.models import Kelas

def main_page(request):
    kelas = Kelas.objects.all()
    if not kelas.exists():
        kelas = None

    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'kelas' : kelas,
            'is_mentor' : False,
            'is_mentee' : False,
        }
        if request.user.role == '1':
            context['is_mentor'] = True
            my_class = Kelas.objects.filter(mentor_kelas=request.user.id)
            if not my_class.exists():
                context['kelas_saya'] = None
            else:
                context['kelas_saya'] = my_class
            return render(request, 'main-page.html', context)
        elif request.user.role == '2':
            my_class = Kelas.objects.filter(mentee_kelas=request.user.id)
            context['is_mentee'] = True
            if not my_class.exists():
                context['kelas_saya'] = None
            else:
                context['kelas_saya'] = my_class
            return render(request, 'main-page.html', context)
        return render(request, 'main-page.html', context)
    else:
        context = {
            'kelas' : kelas
        }
        return render(request, 'main-page.html', context)