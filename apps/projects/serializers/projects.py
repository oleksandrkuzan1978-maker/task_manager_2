from rest_framework import serializers

from apps.projects.models import ProjectFile
from apps.tasks.models import Project

class AllProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'created_at', 'description']

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields=['id', 'title', 'created_at', 'description', 'count_of_files']

class  AllProjectFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'title', 'projects']