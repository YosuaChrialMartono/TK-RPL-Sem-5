from django.db import models
from mentee.models import Mentee
from kelas.models import Kelas  

class Review(models.Model):
    rating = models.IntegerField()
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(Mentee, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='review_kelas')
