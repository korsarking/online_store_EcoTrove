from rest_framework.routers import DefaultRouter

from apps.addresses.views import UserAddressViewSet


router = DefaultRouter(trailing_slash=False)

router.register(r"address", UserAddressViewSet, basename="address")

app_name = "addresses"

urlpatterns = router.urls
