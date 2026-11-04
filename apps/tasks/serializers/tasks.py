"""Сериализаторы списка задач с названием проекта и подробностей задачи с вложенными тегами."""

from rest_framework import serializers

from apps.tasks.models import Task, Priority
from .tags import TagsSerializer
from ...projects.models import Project


class AllTasksSerializer(serializers.ModelSerializer):
    """Краткие данные задачи с названием связанного проекта только для чтения."""
    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    assignee = serializers.SlugRelatedField(read_only=True
                                            , slug_field='email')
    class Meta:
        """Поля модели и параметры сериализации AllTasksSerializer."""
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'project', 'assignee', 'due_date']

class CreateTaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title',
        queryset=Project.objects.all(),)
    class Meta:
        model = Task
        fields = ('title',
 'description',
 'priority',
 'project',
 'tags',
 'due_date')
        def validate_name(self, value: str) -> str:
            if len(value) < 10:
                raise serializers.ValidationError("The name of the task couldn't be less than 10 characters")
            return value

        def validate_description(self, value: str) -> str:
            if len(value) < 50:
                raise serializers.ValidationError("The description of the task couldn't be less than 50 characters")
            return value


class TaskInfoSerializer(serializers.ModelSerializer):
    """Все поля задачи с вложенным представлением тегов."""
    tags = TagsSerializer(many=True)
    class Meta:
        """Поля модели и параметры сериализации TaskInfoSerializer."""
        model = Task
        fields = '__all__'
