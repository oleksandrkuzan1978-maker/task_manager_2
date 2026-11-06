"""API списка, создания, просмотра, изменения и удаления задач."""

from django.db.models import QuerySet
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from apps.tasks.models import Task
from apps.tasks.serializers.tasks import (AllTasksSerializer, CreateUpdateTaskSerializer, TaskDetailSerializer)


class StandardResultsSetPagination(PageNumberPagination):
    """Пагинация задач: пять записей по умолчанию и максимум пятнадцать."""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 15


class TaskListAPIView(APIView):
    """Получение списка задач и создание новой задачи."""
    paginator = StandardResultsSetPagination

    def get_objects(self) -> QuerySet:
        """Вернуть задачи с необязательным фильтром по названию проекта."""
        project_name = self.request.query_params.get('project_name')

        if project_name:
            return Task.objects.filter(project__title=project_name)
        return Task.objects.all()

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Проверить входные данные и создать задачу с ответом 201."""
        serializer = CreateUpdateTaskSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Вернуть страницу задач либо ответ 204 при пустой выборке."""
        tasks = self.get_objects()

        if not tasks.exists():
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)

        paginator = self.paginator()
        page = paginator.paginate_queryset(tasks, request, view=self)

        if page is not None:
            serializer = AllTasksSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = AllTasksSerializer(tasks, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TaskDetailAPIView(RetrieveAPIView):
    # 1. Объявляем атрибут на уровне класса, чтобы DRF не ругался
    """Просмотр, частичное обновление через PUT и удаление задачи."""
    serializer_class = TaskDetailSerializer
    def get_object(self):
        """Найти задачу по ID из URL или вернуть ошибку 404."""
        return get_object_or_404(Task, pk=self.kwargs['pk'])

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Вернуть подробные данные задачи."""
        task = self.get_object()
        # 2. Переменную экземпляра лучше назвать serializer
        serializer = self.serializer_class(task)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """Проверить и сохранить переданные поля существующей задачи."""
        task = self.get_object()
        serializer = CreateUpdateTaskSerializer(instance=task,
                                                data=request.data,
                                                partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Удалить задачу и вернуть статус 204."""
        task = self.get_object()
        task.delete()
        return Response({"message": "The task has been deleted."},
                                status=status.HTTP_204_NO_CONTENT)














