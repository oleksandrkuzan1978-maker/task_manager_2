"""Сериализаторы списка задач с названием проекта и подробностей задачи с вложенными тегами."""

from rest_framework import serializers

from apps.tasks.models import Task
from .tags import TagsSerializer
class AllTasksSerializer(serializers.ModelSerializer):
    """Краткие данные задачи с названием связанного проекта только для чтения."""
    project_title = serializers.CharField(
        source='project.title',
        read_only=True,
        default=None,
    )
    class Meta:
        """Поля модели и параметры сериализации AllTasksSerializer."""
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'project_title']

class TaskInfoSerializer(serializers.ModelSerializer):
    """Все поля задачи с вложенным представлением тегов."""
    tags = TagsSerializer(many=True)
    class Meta:
        """Поля модели и параметры сериализации TaskInfoSerializer."""
        model = Task
        fields = '__all__'
