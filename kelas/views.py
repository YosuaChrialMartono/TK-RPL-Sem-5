from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from .models import Kelas, FormJoinKelas
from authuser.models import User
from mentee.models import Mentee
from mentor.models import Mentor

def get_all_kelas(request):
    judul_kelas = request.GET.get('judul', '')
    print(judul_kelas)

    if judul_kelas == '':
        daftar_kelas = all_kelas()

        serialized_kelas = serialize('json', daftar_kelas)
        response = JsonResponse(serialized_kelas, safe=False)
    else:
        kelas = filter_kelas_by_judul(judul=judul_kelas)
        serialized_kelas = serialize('json', [kelas])

        response = HttpResponse(serialized_kelas, content_type='application/json')

    return response

def get_kelas_by_mentor(request, username_mentor):
    daftar_kelas = filter_kelas_by_mentor(username_mentor)
    
    if daftar_kelas is None:
        return JsonResponse({'error': f"User dengan username {username_mentor} tidak ditemukan."}, status=400)

    serialized_kelas = serialize('json', daftar_kelas)
    json_response = JsonResponse(serialized_kelas, safe=False)

    return json_response

def join_kelas(request, mentee, kelas):
    if kelas.harga_kelas == 0:
        form = FormJoinKelas

def add_mentee(mentee, kelas):
    kelas.mentee_kelas.add(mentee)
    mentee.kelas_mentee.add(kelas)

def filter_kelas_by_judul(judul):
    try:
        kelas = Kelas.objects.get(judul_kelas=judul)
    except Kelas.DoesNotExist:
        return None
    
    return kelas

def filter_kelas_by_mentor(username_mentor):
    try:
        user = User.objects.get(username=username_mentor)
    except User.DoesNotExist:
        return None
    
    mentor = Mentor.objects.get(user=user)
    kelas_list = Kelas.objects.filter(mentor_kelas=mentor)
    
    return kelas_list

def all_kelas():
    return Kelas.objects.all()
