from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.addresses.models import Address
from apps.addresses.serializers import UserAddressSerializer
from apps.users.models import User


class UserAddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["country", "region", "city"]

    def get_queryset(self):
        queryset = super().get_queryset()

        if hasattr(self, "swagger_fake_view"):
            return self.queryset.none()

        if self.request.user.role == User.Role.USER:
            qs = self.queryset.filter(users=self.request.user)
            return qs

        return queryset
