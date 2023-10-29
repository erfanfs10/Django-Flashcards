from django.contrib import admin
from .models import Card


@admin.register(Card)
class AdminCard(admin.ModelAdmin):
    list_display = ("front", "back", "correct_counts", "incorrect_counts",
                     "review_counts", "box_number", "next_review", "learned", "created")
    list_filter = ("learned", "box_number")
    list_editable = ("next_review",)