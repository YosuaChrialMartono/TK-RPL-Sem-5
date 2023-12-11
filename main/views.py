from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from kelas.models import Kelas
import kelas.views as kelas_func

@login_required(login_url='authuser:login')
def main_page(request):
    kelas = kelas_func.all_kelas()
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
            kelas_diikuti = kelas_func.filter_kelas_diikuti(request.user)
            context['is_mentee'] = True
            if not kelas_diikuti:
                context['kelas_diikuti'] = None
            else:
                context['kelas_diikuti'] = kelas_diikuti
            return render(request, 'main-page.html', context)
        return render(request, 'main-page.html', context)
    else:
        return render(request, 'main-page.html')