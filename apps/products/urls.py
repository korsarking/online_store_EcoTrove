from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet
from apps.products.views import ProductAttachmentsViewSet
from apps.products.views import ProductReviewViewSet
from apps.products.views import ProductViewSet
from apps.products.views import SubCategoryViewSet

router = DefaultRouter()

app_name = "products"

router.register("product", ProductViewSet, "product")
router.register("product_attachments", ProductAttachmentsViewSet, "attachments")
router.register("product_review", ProductReviewViewSet, "review")
router.register("product_category", CategoryViewSet, "category")
router.register("product_sub_category", SubCategoryViewSet, "subcategory")

urlpatterns = router.urls
