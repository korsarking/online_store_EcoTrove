from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "full_name",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "role",
            "groups",
            "user_permissions",
            "addresses",
        ]

    @staticmethod
    def get_full_name(obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        user = super().create(validated_data)

        user.set_password(validated_data["password"])
        user.save()
        return user


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_pic",)
