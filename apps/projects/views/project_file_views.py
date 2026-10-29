"""API списка файлов с фильтром по названию проекта и загрузки файла в указанный проект."""

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListAPIView

from apps.projects.models import ProjectFile, Project
from apps.projects.serializers.project_file_serializers import (AllProjectFilesSerializer, CreateProjectFileSerializer,)

class ProjectFileListAPIView(APIView):
    """Просмотр файлов по названию проекта и загрузка файла с привязкой к проекту по ID."""
    def get_objects(self,project_name=None):
        """Вернуть все файлы либо файлы проекта с точным совпадением названия."""
        if project_name:
            project_file = ProjectFile.objects.filter(projects__title=project_name)
            return project_file
        return ProjectFile.objects.all()

    def get(self, request: Request) -> Response:
        """Вернуть файлы с необязательным параметром project — точным названием проекта.

        Непустой список возвращается с кодом 200; при пустой выборке возвращает [] и код 404.
        """
        project_name = request.query_params.get('project')
        project_files = self.get_objects(project_name)

        if not project_files.exists():
            return Response(data=[], status=status.HTTP_404_NOT_FOUND)

        serializer = AllProjectFilesSerializer(project_files, many=True, context={'request': request},)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request: Request) -> Response:

        """Загрузить multipart-файл и связать его с проектом по положительному project_id.

        Ожидает поля title, file и project_id; файл передаёт сериализатору как raw_file.
        Успех возвращает 201, ошибки входных данных — 400, отсутствующий проект — 404.
        """
        file_content = request.FILES.get("file")

        try:
            project_id = serializers.IntegerField(
                min_value=1
            ).run_validation(request.data.get('project_id'))
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({
                'project_id': exc.detail
            })

        project = get_object_or_404(Project, pk=project_id)

        serializer = CreateProjectFileSerializer(data=request.data, context={"raw_file": file_content},)
        if serializer.is_valid():
            project_file = serializer.save()
            project_file.projects.set([project])
            return Response(data={"message": "File upload successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)





