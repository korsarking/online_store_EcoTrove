from django.contrib.auth import get_user_model
from drf_util.utils import gt
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.users.models import UserAddress
from apps.users.serializers import UserAddressSerializer

User = get_user_model()


class UserAddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["country", "region", "city"]

    def get_queryset(self):
        qs = self.queryset

        if hasattr(self, "swagger_fake_view"):
            qs = self.queryset.none()

        if gt(self.request.user, "role") == User.Role.USER:
            qs = self.queryset.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
