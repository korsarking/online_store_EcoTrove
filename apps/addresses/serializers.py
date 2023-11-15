from rest_framework import serializers

from apps.addresses.models import Address


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        instance = self.Meta.model._default_manager.create(**validated_data)
        user = self.context["request"].user
        instance.users.add(user)
        return instance
