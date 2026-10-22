from django.utils import timezone
from rest_framework import serializers

from apps.tasks.models import Project

class AllProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description']
