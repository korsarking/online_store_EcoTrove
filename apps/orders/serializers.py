from django.db.models import DecimalField
from django.db.models import F
from django.db.models import Sum
from rest_framework import serializers

from apps.addresses.serializers import UserAddressSerializer
from apps.orders.models import Cart
from apps.orders.models import CartItem
from apps.orders.models import Order
from apps.products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "user",
            "cart",
            "status",
            "total",
        ]


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "created_at", "updated_at", "user", "cart", "status", "total"]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "user",
            "cart",
            "total",
            "address",
        ]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "user",
            "is_archived",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "created_at",
            "updated_at",
            "product",
            "price",
            "discount",
            "count",
        ]

        read_only_fields = ["id", "created_at", "updated_at", "price", "discount"]


class CartItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "created_at",
            "updated_at",
            "product",
            "price",
            "discount",
            "count",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "price",
            "discount",
            "product",
        ]


class CartDetailsSerializer(serializers.ModelSerializer):
    items = CartItemDetailSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "created_at",
            "updated_at",
            "is_archived",
            "items",
            "total",
        ]

    def get_total(self, obj):
        total = obj.items.aggregate(
            total=Sum(
                F("product__price")
                * ((100 - F("product__discount")) / 100.0)
                * F("count"),
                output_field=DecimalField(),
            )
        ).get("total")
        return total


class OrderDetailSerializer(serializers.ModelSerializer):
    cart = CartDetailsSerializer(read_only=True)
    address = UserAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "user",
            "cart",
            "status",
            "total",
        ]
