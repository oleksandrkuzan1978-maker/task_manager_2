from rest_framework import serializers

from apps.tasks.models import Task
from .tags import TagsSerializer
class AllTasksSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(
        source='project.title',
        read_only=True,
        default=None,
    )
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'project_title']

class TaskInfoSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    class Meta:
        model = Task
        fields = '__all__'
