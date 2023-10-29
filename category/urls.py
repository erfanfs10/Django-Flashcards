from django.urls import path
from .views import CategoryList, CategoryView, CategoryAdd


urlpatterns = [
    path("", CategoryList.as_view(), name="category-list"),
    path("<str:category_name>/", CategoryView.as_view(), name="category-view"),
    path("add/", CategoryAdd.as_view(), name="category-add")
]
