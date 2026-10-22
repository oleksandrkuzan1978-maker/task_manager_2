from django.utils import timezone
from rest_framework import serializers

from apps.tasks.models import Task

class AllTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority']

