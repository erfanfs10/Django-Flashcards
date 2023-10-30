from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    created = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ("category", "front", "back", "us_pronunciation", "uk_pronunciation",
                  "correct_counts", "incorrect_counts", "review_counts",
                  "box_number", "next_review", "learned", "created")

    def get_created(self, obj):
        return obj.created.date()
    