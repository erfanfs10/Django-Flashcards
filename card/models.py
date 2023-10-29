from django.db import models
from django.utils import timezone
from category.models import Category

class Card(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="cards")
    front = models.TextField()
    back = models.TextField()
    us_pronunciation = models.FileField(upload_to="words_us_pronunciation", default="undefined.aac")
    uk_pronunciation = models.FileField(upload_to="words_uk_pronunciation", default="undefined.aac")
    correct_counts = models.PositiveSmallIntegerField(default=0)
    incorrect_counts = models.PositiveSmallIntegerField(default=0)
    review_counts = models.PositiveSmallIntegerField(default=0)
    box_number = models.PositiveSmallIntegerField(default=1)
    next_review = models.DateTimeField(default=timezone.now, editable=True)
    learned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.front
