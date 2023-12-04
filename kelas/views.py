from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from .models import Kelas, FormJoinKelas
from authuser.models import User
from mentee.models import Mentee
from mentor.models import Mentor
from mentee.decorators import mentee_required
from mentor.decorators import mentor_required

def get_all_kelas(request):
    judul_kelas = request.GET.get('kelas', '')
    mentor = request.GET.get('mentor', '')

    if mentor == '':
        daftar_kelas_mentor = all_kelas()
    else:
        daftar_kelas_mentor = filter_kelas_by_mentor(mentor)
        if daftar_kelas_mentor is None:
            return JsonResponse({'error': f"Mentor dengan username {mentor} tidak ditemukan."}, status=400)

    if judul_kelas == '':
        daftar_kelas_judul = all_kelas()
    else:
        daftar_kelas_judul = filter_kelas_by_judul(judul=judul_kelas)
        if daftar_kelas_judul is None:
            return JsonResponse({'error': f"Kelas dengan judul {judul_kelas} tidak ditemukan."}, status=400)
    
    daftar_kelas = [value for value in daftar_kelas_mentor if value in daftar_kelas_judul]
    serialized_kelas = serialize('json', daftar_kelas)
    response = JsonResponse(serialized_kelas, safe=False)

    return response

def get_kelas_by_mentor(request, username_mentor):
    daftar_kelas = filter_kelas_by_mentor(username_mentor)
    
    if daftar_kelas is None:
        return JsonResponse({'error': f"User dengan username {username_mentor} tidak ditemukan."}, status=400)

    serialized_kelas = serialize('json', daftar_kelas)
    json_response = JsonResponse(serialized_kelas, safe=False)

    return json_response

def get_form_by_kelas(request, idKelas):
    form = filter_form_by_kelas(idKelas)
    if form is None:
        return HttpResponse(status=400, content=f'Kelas dengan id {idKelas} tidak ditemukan')
    
    serialized_form = serialize('json', form)
    response = JsonResponse(serialized_form, safe=False)
    
    return response

def get_form_by_id(request, idKelas, idForm):
    form = filter_form_by_id(idForm)
    if form is None:
        return HttpResponse(status=400, content=f'Form dengan id {idForm} tidak ditemukan')
    
    serialized_form = serialize('json', [form])
    response = JsonResponse(serialized_form, safe=False)
    
    return response

def join_kelas(request, mentee, kelas):
    # Cek apakah kapasitas tersedia
    if kelas.jumlah_mentee >= kelas.kapasitas_maksimal:
        return HttpResponse(status=409, content="Kelas sudah penuh, tidak dapat bergabung.")
    
    # Cek apakah mentee sudah terdaftar di kelas
    if kelas.mentee_kelas.filter(user=mentee.user).exists():
        return HttpResponse(status=409, content="Anda sudah terdaftar di kelas ini.")
    
    # Cek apakah terdapat form pendaftaran dengan status "Menunggu Pembayaran"
    menunggu_pembayaran = check_form_if_status(mentee=mentee, kelas=kelas, status='Menunggu Pembayaran')
    if menunggu_pembayaran:
        return HttpResponse(status=409, content="Anda sudah memiliki form pendaftaran dengan status menunggu pembayaran. Silahkan lakukan pembayaran kepada mentor dan konfirmasi")

    # Cek apakah terdapat form pendaftaran dengan status "Menunggu Konfirmasi"
    menunggu_konfirmasi = check_form_if_status(mentee=mentee, kelas=kelas, status='Menunggu Pembayaran')
    if menunggu_konfirmasi:
        return HttpResponse(status=409, content="Anda sudah memiliki form pendaftaran dengan status menunggu konfirmasi. Silahkan menunggu konfirmasi mentor")
    
    if kelas.harga_kelas == 0:
        form = FormJoinKelas(pendaftar=mentee, kelas=kelas, status_pembayaran='Kelas Gratis')
        form.save()

        add_mentee(mentee, kelas)

        return HttpResponse(status=200, content=f"Berhasil join ke kelas {kelas.judul_kelas}")
    
    form = FormJoinKelas(pendaftar=mentee, kelas=kelas)
    form.save()

    return HttpResponse(status=200, content=f"Berhasil membuat form pendaftaran. Silahkan melakukan konfirmasi pembayaran")

def update_status(request, form, mentee, kelas, status_konfirmasi):
    if status_konfirmasi == 'tolak':
        form.status_pembayaran = 'Pembayaran Ditolak'
        form.save()
        return HttpResponse(status=200, content=f'Berhasil menolak konfirmasi')
    
    form.status_pembayaran = 'Pembayaran Diterima'
    form.save()
    add_mentee(mentee, kelas)

    return HttpResponse(status=200, content=f'Berhasil menerima konfirmasi')

# ============================== helper function =================================
# lol bad documentation

def add_mentee(mentee, kelas):
    kelas.mentee_kelas.add(mentee)
    kelas.jumlah_mentee += 1
    kelas.save()

def check_form_if_status(mentee, kelas, status):
    return FormJoinKelas.objects.filter(pendaftar=mentee, kelas=kelas, status_pembayaran=status).exists()

def get_kelas_by_id(idKelas):
    try:
        kelas = Kelas.objects.get(id=idKelas)
    except Kelas.DoesNotExist:
        return None
    
    return kelas

def filter_kelas_by_judul(judul):
    try:
        kelas = Kelas.objects.filter(judul_kelas=judul)
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

def filter_form_by_id(id):
    try:
        form = FormJoinKelas.objects.get(id=id)
    except FormJoinKelas.DoesNotExist:
        return None
    
    return form

def filter_form_by_kelas(idKelas):
    kelas = get_kelas_by_id(idKelas)
    if kelas is None:
        return None
    
    form = FormJoinKelas.objects.filter(kelas=kelas)
    
    return form

def all_kelas():
    return Kelas.objects.all()

def all_form():
    return FormJoinKelas.objects.all()