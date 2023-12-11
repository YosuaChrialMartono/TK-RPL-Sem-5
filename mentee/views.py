from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.core.serializers import serialize
from mentee.models import Mentee
from .decorators import mentee_required
import kelas.views as kelas_func
from kelas.forms import PembayaranForm

@mentee_required(login_url='authuser:login')
def mentee_home(request):
    return render(request, 'mentee-home.html')

@mentee_required(login_url='authuser:login')
def show_all_kelas(request):
    classes = kelas_func.all_kelas()

    return render(request, 'show-all-kelas.html', {'semua_kelas': classes})

@mentee_required(login_url='authuser:login')
def show_form_pendaftaran(request):
    forms = kelas_func.filter_form_by_mentee(request.user.id)

    return render(request, 'show-form-pembayaran.html', {'forms': forms})

@mentee_required(login_url='authuser:login')
def show_form_pendaftaran_by_formId(request):
    forms = kelas_func.filter_form_by_mentee(request.user.id)

    return render(request, 'show-form-pembayaran.html', {'forms': forms})

@mentee_required(login_url='authuser:login')
def join_kelas(request):
    id_kelas = request.GET.get('kelasid', '')
    if id_kelas == '':
        return HttpResponseBadRequest('Tidak ada parameter nama kelas yang ingin diikuti')

    kelas = kelas_func.get_kelas_by_id(idKelas=id_kelas)
    if kelas is None:
        return HttpResponseBadRequest('Kelas yang ingin diikuti tidak ada')
    
    try:
        mentee = Mentee.objects.get(user=request.user)
    except Mentee.DoesNotExist:
        return HttpResponseNotFound('Mentee tidak ditemukan')

    response = kelas_func.join_kelas(request, mentee, kelas)

    return response

@mentee_required(login_url='authuser:login')
def add_bukti_pembayaran(request, idForm):
    form_pendaftaran = kelas_func.filter_form_by_id(idForm)
    if form_pendaftaran is None:
        return HttpResponseNotFound('Form tidak ditemukan') 
    
    if request.method == 'POST':
        form = PembayaranForm(request.POST, user=request.user)
        if form.is_valid():
            form.clean()
            print(form.cleaned_data.get('url_bukti_pembayaran'))
            form_pendaftaran.url_bukti_pembayaran = form.cleaned_data.get('url_bukti_pembayaran')
            form_pendaftaran.status_pembayaran = 'Menunggu Konfirmasi'
            form_pendaftaran.save()
            return redirect(f'mentee:form_by_id', idForm=idForm)
    else:
        form = PembayaranForm()

    return render(request, 'add-bukti-pembayaran.html', {'form': form, 'idForm': idForm}) 

def get_form_by_id(request, idForm):
    form = kelas_func.filter_form_by_id(idForm)
    if form is None:
        return HttpResponse(status=400, content=f'Form dengan id {idForm} tidak ditemukan')
    
    serialized_form = serialize('json', [form])
    response = JsonResponse(serialized_form, safe=False)
    
    return response