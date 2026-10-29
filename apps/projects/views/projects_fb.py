"""Главная страница и функциональные API-представления списка, создания, изменения и удаления проектов."""


from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime

from apps.projects.serializers import AllProjectsSerializer, ProjectDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.tasks.models import Project
from django.http import HttpResponse

"""Текстовая главная страница проекта."""
def index(request):
    """Вернуть HTTP-ответ с текстом «Главная страница»."""
    return HttpResponse("Главная страница")

##Закончили на Задании 7 (Adpractice_Pr5, стр. 43-44)
def get_objects(date_from=None, date_to=None):
    """Вернуть проекты с фильтром created_at между двумя датами YYYY-MM-DD включительно.

    Фильтр применяется только при наличии обеих дат; границы соответствуют полуночи.
    Некорректная строка даты вызывает ValueError; одна указанная дата не ограничивает выборку.
    """
    if date_from and date_to:
        date_from = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
        date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d'))

        projects = Project.objects.filter(created_at__range=[date_from, date_to])
        return projects
    return Project.objects.all()


@api_view(['GET', 'POST'])
def get_all_create_projects(request: Response) -> Response:
    """Обработать GET списка проектов или POST создания проекта.

    GET принимает date_from и date_to в формате YYYY-MM-DD и возвращает 200 либо 204 при пустой выборке.
    POST проверяет данные сериализатором и возвращает 201 при создании либо 400 при ошибках.
    """
    if request.method == 'GET':
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        projects = get_objects(date_from, date_to)
        if not projects.exists():
            return Response({'Projects': 'Projects not found'}
                            , status=status.HTTP_204_NO_CONTENT)
        serializer=AllProjectsSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = AllProjectsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_project(pk:int):
    """Найти проект по первичному ключу или вызвать Http404, если записи нет."""
    return get_object_or_404(Project, pk=pk)

@api_view(['GET', 'PUT', 'DELETE'])
def get_patch_delete_project(request: Response, pk:int) -> Response:
    """Получить, частично обновить через PUT или удалить проект по pk.

    GET и успешный PUT возвращают 200, DELETE — 204; отсутствующий проект даёт 404.
    Несмотря на имя функции, PATCH не входит в разрешённые методы.
    """
    if request.method == 'GET':
        project = get_project(pk)
        serializer= ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        project = get_project(pk=pk)
        serializer = ProjectDetailSerializer(instance=project, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        project = get_project(pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









