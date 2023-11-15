from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

app_name = "users"

urlpatterns = router.urls

urlpatterns += [
    path(r"auth/", include("djoser.urls")),
    path(r"auth/", include("djoser.urls.jwt")),
]
