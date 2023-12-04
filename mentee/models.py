from django.db import models

from authuser.models import User
from kelas.models import Kelas

class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    enrolled_classes = models.ManyToManyField(Kelas, related_name='kelas_diikuti')
