from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from apps.users.views import UserAddressViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"address", UserAddressViewSet, basename="address")

urlpatterns = router.urls

app_name = "users"

urlpatterns += [
    path(r"auth/", include("djoser.urls")),
    path(r"auth/", include("djoser.urls.jwt")),
]
