from django.urls import path
from .views import (CategoryList, CategoryDetail, CategoryAdd,
                     CategoryRename, CategoryDelete)


urlpatterns = [
    path("list/", CategoryList.as_view(), name="category-list"),
    path("detail/", CategoryDetail.as_view(), name="category-detail"),
    path("create/", CategoryAdd.as_view(), name="category-add"),
    path("rename/", CategoryRename.as_view(), name="category-rename"),
    path("delete/", CategoryDelete.as_view(), name="category-delete")
]
