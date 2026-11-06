"""Сериализаторы списка и подробностей проектов, а также связей файлов с проектами."""

from rest_framework import serializers

from apps.projects.models import ProjectFile
from apps.tasks.models import Project


class AllProjectsSerializer(serializers.ModelSerializer):
    """Преобразование ID, названия, даты создания и описания проекта и проверка входных данных."""
    class Meta:
        """Поля модели и параметры сериализации AllProjectsSerializer."""
        model = Project
        fields = ['id', 'title', 'created_at', 'description']


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Данные проекта с вычисляемым количеством связанных файлов."""
    class Meta:
        """Поля модели и параметры сериализации ProjectDetailSerializer."""
        model = Project
        fields=['id', 'title', 'created_at', 'description', 'count_of_files']


class  AllProjectFilesSerializer(serializers.ModelSerializer):
    """ID, название файла и ID связанных проектов."""
    class Meta:
        """Поля модели и параметры сериализации AllProjectFilesSerializer."""
        model = ProjectFile
        fields = ['id', 'title', 'projects']


class CreateProjectSerializer(serializers.ModelSerializer):
    """Обновление описания проекта с представлением файлов только для чтения."""
    files = AllProjectFilesSerializer(many=True, read_only=True)
    class Meta:
        """Поля проекта; название и дата создания доступны только для чтения."""
        model = Project
        fields = ['title', 'description', 'created_at', 'files']
        read_only_fields = ('title', 'created_at',)


class ProjectShortInfoSerializer(serializers.ModelSerializer):
    """Краткое представление проекта: ID и название."""
    class Meta:
        """Модель проекта и поля краткого представления."""
        model = Project
        fields = ('id', 'title')
