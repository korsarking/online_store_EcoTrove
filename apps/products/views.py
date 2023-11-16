from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsAdmin
from apps.common.permissions import IsAdminOrOwner
from apps.common.permissions import ReadOnly
from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductAttachments
from apps.products.models import ProductReview
from apps.products.models import SubCategory
from apps.products.serializers import CategorySerializer
from apps.products.serializers import ProductAttachmentsSerializer
from apps.products.serializers import ProductReviewSerializer
from apps.products.serializers import ProductSerializer
from apps.products.serializers import SubCategorySerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin | ReadOnly)
    filterset_fields = ("sub_category",)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin | ReadOnly)
    parser_classes = (MultiPartParser,)


class SubCategoryViewSet(ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin | ReadOnly)
    filterset_fields = ("category",)
    parser_classes = (MultiPartParser,)


class ProductReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializer
    queryset = ProductReview.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrOwner | ReadOnly)
    filterset_fields = (
        "product",
        "rating",
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductAttachmentsViewSet(ModelViewSet):
    serializer_class = ProductAttachmentsSerializer
    queryset = ProductAttachments.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin | ReadOnly)
    parser_classes = (MultiPartParser,)
    filterset_fields = ("product",)
