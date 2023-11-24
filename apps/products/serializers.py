from rest_framework import serializers

from apps.products.models import Category
from apps.products.models import SubCategory
from apps.products.models import Products
from apps.products.models import ProductAttachments
from apps.products.models import ProductReview


class ProductAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttachments
        fields = (
            "id",
            "created_at",
            "updated_at",
            "attachment",
            "product",
        )

        read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    attachments = ProductAttachmentsSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = "__all__"

        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

        read_only_fields = ["id", "created_at", "updated_at"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

        read_only_fields = ["id", "created_at", "updated_at"]


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "user",
        ]
