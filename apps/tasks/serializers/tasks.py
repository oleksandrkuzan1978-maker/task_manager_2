"""Сериализаторы списка задач с названием проекта и подробностей задачи с вложенными тегами."""
from typing import Any

from django.utils import timezone

from django.core.checks import Tags
from rest_framework import serializers

from apps.tasks.models import Task, Priority
from .tags import TagsSerializer
from apps.projects.serializers import ProjectShortInfoSerializer
from ...projects.models import Project
from apps.users.models import User


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


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    """Валидация, создание и обновление задачи с проектом и тегами."""
    project = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Project.objects.all(), )

    assignee = serializers.SlugRelatedField(slug_field='email'
                                            , queryset=User.objects.all()
                                            , required=False)


    class Meta:
        """Модель задачи и поля, доступные для записи."""
        model = Task
        fields = ('title',
                  'description',
                  'priority',
                  'project',
                  'tags',
                  'due_date',
                  'assignee')

    def validate_name(self, value: str) -> str:
        """Проверить длину названия; DRF не вызывает метод без поля name."""
        if len(value) < 10:
            raise serializers.ValidationError("The name of the task couldn't be less than 10 characters")
        return value

    def validate_description(self, value: str) -> str:
        """Отклонить описание короче 50 символов."""
        if len(value) < 50:
            raise serializers.ValidationError("The description of the task couldn't be less than 50 characters")
        return value

    def validate_project(self, value: str) -> str:
        """Проверить существование выбранного проекта."""
        if not Project.objects.filter(title=value).exists():
            raise serializers.ValidationError("The project name doesn't exist")
        return value

    def validate_tags(self, value: list[str, ...]) -> list[str, ...]:
        """Проверить существование переданных тегов."""
        if not Tags.objects.filter(name__in=value).exists():
            raise serializers.ValidationError("The tag name doesn't exist")
        return value

    def validate_due_date(self, value ):
        # Замените строку 65 на безопасный вариант:
        """Добавить часовой пояс при необходимости и отклонить прошедший срок."""
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.get_current_timezone())

        if value < timezone.now():
            raise serializers.ValidationError("The due date can't be in the future")
        return value

    def create(self, validated_data: dict[str, Any]) -> Task:
        """Сохранить новую задачу и добавить переданные теги."""
        tags = validated_data.pop('tags', [])

        task = Task.objects.create(**validated_data)

        for tag in tags:
            task.tags.add(tag)

        task.save()
        return task

    def update(self, instance: Task, validated_data: dict[str, Any]) -> Task:
        """Обновить переданные поля задачи и добавить указанные теги."""
        tags = validated_data.pop('tags', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags:
            for tag in tags:
                instance.tags.add(tag)
        instance.save()
        return instance


class TaskInfoSerializer(serializers.ModelSerializer):
    """Все поля задачи с вложенным представлением тегов."""
    tags = TagsSerializer(many=True)

    class Meta:
        """Поля модели и параметры сериализации TaskInfoSerializer."""
        model = Task
        fields = '__all__'

class TaskDetailSerializer(serializers.ModelSerializer):
    """Подробности задачи с вложенными данными проекта и тегов."""
    project = ProjectShortInfoSerializer()
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        """Поля задачи без времени обновления и удаления."""
        model = Task
        exclude =('updated_at', 'deleted_at')