from django.urls import path, include

urlpatterns = [
    path("api/", include("api.account.urls")),
    path("api/", include("api.products.urls"))
]