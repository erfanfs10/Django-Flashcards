from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("account.urls")),
    path("card/", include("card.urls")),
    path("category/", include("category.urls"))
]
