"""Сериализаторы выдачи файлов и ручного сохранения загруженного файла."""

from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers
from apps.projects.models import ProjectFile
from apps.projects.utils.upload_file_helpers import (
    ALLOWED_EXTENSIONS,
    check_extension,
    create_file_path,
    check_file_size,
    save_file
)

class AllProjectFilesSerializer(serializers.ModelSerializer):
    """ID, название, путь файла и ID связанных проектов."""
    class Meta:
        """Поля модели и параметры сериализации AllProjectFilesSerializer."""
        model = ProjectFile
        fields = ('id', 'title', 'file', 'projects')


class CreateProjectFileSerializer(serializers.ModelSerializer):
    """Входные поля title и file и ручное сохранение файла из context["raw_file"]."""
    class Meta:
        """Поля модели и параметры сериализации CreateProjectFileSerializer."""
        model = ProjectFile
        fields = ('title', 'file',)

    def validate_file_name(self, value: UploadedFile) -> UploadedFile:
        """Проверить ASCII-имя и допустимое расширение переданного UploadedFile.

        При нарушении вызывает serializers.ValidationError. Автоматически DRF этот метод
        не вызывает: поле file_name не объявлено, а загружаемое поле называется file.
        """
        if not value.name.isascii():
            raise serializers.ValidationError("Please, provide a valid file name.")

        if not check_extension(value.name):
            raise serializers.ValidationError(
                f"Valid file extensions: {ALLOWED_EXTENSIONS}")
        return value

    def create(self, validated_data):
        """Сохранить файл из context["raw_file"] и создать запись ProjectFile из проверенных данных.

        Имя берёт из validated_data["file"].name. При отсутствии raw_file или размере свыше 2 МиБ
        вызывает serializers.ValidationError. Записывает относительный путь в поле file.
        Физический файл при последующей ошибке создания записи автоматически не удаляется.
        """
        file_name = validated_data['file'].name
        raw_file = self.context.get('raw_file')

        if raw_file is None:
            raise serializers.ValidationError({'file': 'No file was provided.'})

        if check_file_size(file=raw_file):
            file_path = create_file_path(file_name=file_name)
            save_file(file_path=file_path, file_content=raw_file)

            validated_data['file'] = file_path

            return ProjectFile.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("File size is too large (2 MB as maximum)."
)