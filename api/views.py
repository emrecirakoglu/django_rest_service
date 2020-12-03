from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import ClientSerializer, TaskLogSerializer
from api.models import Client, TaskLog
import django_filters.rest_framework


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.all().order_by('hostname')
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]


class TaskLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskLog.objects.all().order_by('created_at')
    serializer_class = TaskLogSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status', 'task_type', 'client']
