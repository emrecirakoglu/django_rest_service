from rest_framework import serializers
from api.models import Client, TaskLog


class TaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLog
        fields = '__all__'
        depth = 0


class ClientSerializer(serializers.ModelSerializer):
    task_logs = TaskLogSerializer(many=True)

    class Meta:
        model = Client
        fields = '__all__'
