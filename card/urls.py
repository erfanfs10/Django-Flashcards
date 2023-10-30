from django.urls import path
from .views import (CardCreate, CardDelete, CardDetail, CardEdit)


urlpatterns = [
    path("detail/", CardDetail.as_view(), name="card-detail"),
    path("create/", CardCreate.as_view(), name="card-create"),
    path("delete/", CardDelete.as_view(), name="card-delete"),
    path("edit/", CardEdit.as_view(), name="card-edit")
]