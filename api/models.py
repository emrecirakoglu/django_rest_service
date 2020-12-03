from django.db import models
from api.Task.enums.task_types import TaskType
from api.Task.enums.status import Status


class Client(models.Model):
    routing_key = models.CharField(max_length=512, blank=True, null=True)
    ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=50)
    hash = models.CharField(max_length=512, blank=True, null=True)


class TaskLog(models.Model):
    # user =
    client = models.ForeignKey(Client, related_name="task_logs", on_delete=models.CASCADE, null=True, blank=True)
    task_type = models.CharField(max_length=255, choices=TaskType.choices(), null=True)
    status = models.CharField(max_length=255, choices=Status.choices(), default=Status.PENDING.value)
    message = models.CharField(max_length=255, null=True, blank=True, default=None)
    data = models.CharField(max_length=1024, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(editable=False, null=True, blank=True, default=None, primary_key=False)

