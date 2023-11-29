from django.db import models
from authuser.models import Mentor

# Create your models here.

class Kelas(models.Model):
    judul_kelas = models.CharField(max_length=200)
    tanggal_kelas = models.DateField(auto_now=False, auto_now_add=False)
    harga_kelas = models.IntegerField(default=0)
    mentor_kelas = models.ForeignKey(Mentor, on_delete=models.CASCADE)