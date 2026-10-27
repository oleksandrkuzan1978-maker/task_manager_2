"""Сериализатор всех полей модели тега."""

from rest_framework import serializers

from apps.tasks.models import Tag
class TagsSerializer(serializers.ModelSerializer):
    """Преобразование всех полей тега и проверка данных при создании или изменении."""
    class Meta:
        """Поля модели и параметры сериализации TagsSerializer."""
        model = Tag
        fields = '__all__'