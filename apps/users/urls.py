from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from apps.users.views import FileUploadView

router = DefaultRouter(trailing_slash=False)
router.register("auth/profile_picture", FileUploadView, "profile-picture")

app_name = "users"

urlpatterns = router.urls

urlpatterns += [
    path(r"auth/", include("djoser.urls")),
    path(r"auth/", include("djoser.urls.jwt")),
]
