from rest_framework.routers import DefaultRouter

from apps.orders.views import OrderViewSet
from apps.orders.views import CartViewSet

router = DefaultRouter()

router.register("order", OrderViewSet, "order")
router.register("cart", CartViewSet, "cart")

urlpatterns = router.urls
