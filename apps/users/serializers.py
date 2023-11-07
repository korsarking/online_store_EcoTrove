from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.users.models import UserAddress

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "role",
            "user_permissions",
        ]
        extra_kwargs = {"full_name": {"read_only": True}}

    @staticmethod
    def get_full_name(obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"

        read_only_fields = ["created_at", "updated_at", "user"]
