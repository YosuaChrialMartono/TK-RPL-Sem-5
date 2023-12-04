from django.db import models

from authuser.models import User

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    verification_status = models.BooleanField(default=False)
    verification_document = models.CharField(max_length=255)