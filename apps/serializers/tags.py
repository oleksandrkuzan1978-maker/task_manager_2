from rest_framework import serializers

from apps.tasks.models import Tag
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'