from django.http import JsonResponse
from django.core.serializers import serialize
from .models import Kelas
from authuser.models import Mentor, User

def get_all_kelas(request):
    daftar_kelas = all_kelas()

    serialized_kelas = serialize('json', daftar_kelas)
    json_response = JsonResponse(serialized_kelas, safe=False)

    return json_response

def get_kelas_by_mentor(request, username_mentor):
    try:
        daftar_kelas = filter_kelas_by_mentor(username_mentor)
    except User.DoesNotExist:
        # Mengembalikan respons HTTP 400 jika user dengan username tertentu tidak ditemukan
        return JsonResponse({'error': f"User dengan username {username_mentor} tidak ditemukan."}, status=400)

    serialized_kelas = serialize('json', daftar_kelas)
    json_response = JsonResponse(serialized_kelas, safe=False)

    return json_response

def filter_kelas_by_mentor(username_mentor):
    try:
        user = User.objects.get(username=username_mentor)
    except Exception as e:
        raise e
    
    mentor = Mentor.objects.get(user=user)
    kelas_list = Kelas.objects.filter(mentor_kelas=mentor)
    
    return kelas_list

def all_kelas():
    return Kelas.objects.all()
