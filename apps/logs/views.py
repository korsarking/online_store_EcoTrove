from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.common.permissions import IsAdmin
from apps.logs.models import Log
from apps.logs.serializers import LogSerializer


class LogViewSet(GenericViewSet, ListModelMixin):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )
    filterset_fields = ("event_type",)
