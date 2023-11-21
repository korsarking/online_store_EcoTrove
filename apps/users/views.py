from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.common.permissions import IsAdminOrItself
from apps.common.permissions import ReadOnly
from apps.users.models import User
from apps.users.serializers import ProfileImageSerializer


class FileUploadView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = ProfileImageSerializer
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsAdminOrItself | ReadOnly,
    )
    parser_classes = (MultiPartParser,)
