from django.db import models
from mentor.models import Mentor

class Materi(models.Model):
    judul_materi = models.CharField(max_length=200)
    deskripsi = models.TextField()
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    status_persetujuan = models.CharField(max_length=20, default='Menunggu Persetujuan')
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.judul_materi

    @property
    def is_approved(self):
        return self.status_persetujuan != 'Menunggu Persetujuan'