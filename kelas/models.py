from django.db import models
from mentee.models import Mentee
from mentor.models import Mentor

class Kelas(models.Model):
    judul_kelas = models.CharField(max_length=200)
    tanggal_kelas = models.DateField(auto_now=False, auto_now_add=False)
    harga_kelas = models.IntegerField(default=0)
    mentor_kelas = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    kapasitas_maksimal = models.IntegerField(default=1)
    jumlah_mentee = models.IntegerField(default=0)
    mentee_kelas = models.ManyToManyField(Mentee, related_name='kelas_diikuti', blank=True, default=None)

class FormJoinKelas(models.Model):
    pendaftar = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    url_bukti_pembayaran = models.URLField()
    STATUS_PEMBAYARAN_CHOICES = [
        ('Menunggu Pembayaran', 'Menunggu Pembayaran'),
        ('Menunggu Konfirmasi', 'Menunggu Konfirmasi'),
        ('Pembayaran Diterima', 'Pembayaran Diterima'),
        ('Pembayaran Ditolak', 'Pembayaran Ditolak'),
        ('Kelas Gratis', 'Kelas Gratis'),
    ]
    status_pembayaran = models.CharField(
        max_length=20,
        choices=STATUS_PEMBAYARAN_CHOICES,
        default='Menunggu Pembayaran',
    )
    tanggal_pendaftaran = models.DateTimeField(auto_now_add=True)