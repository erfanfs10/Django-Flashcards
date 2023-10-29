from django.contrib import admin
from .models import Category


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("name", "user", "created")
    