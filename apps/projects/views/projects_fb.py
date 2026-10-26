from django.core.signals import request_started
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime

from django.utils.formats import date_format
from rest_framework.utils.representation import serializer_repr

from apps.projects.serializers import AllProjectsSerializer, ProjectDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.tasks.models import Project
from django.http import HttpResponse

"""Текстовая главная страница проекта."""
def index(request):
    """Вернуть текст главной страницы проекта."""
    return HttpResponse("Главная страница")

##Закончили на Задании 7 (Adpractice_Pr5, стр. 43-44)
def get_objects(date_from=None, date_to=None):
    if date_from and date_to:
        date_from = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
        date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d'))

        projects = Project.objects.filter(created_at__range=[date_from, date_to])
        return projects
    return Project.objects.all()


@api_view(['GET', 'POST'])
def get_all_create_projects(request: Response) -> Response:
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
    return get_object_or_404(Project, pk=pk)

@api_view(['GET', 'PUT', 'DELETE'])
def get_patch_delete_project(request: Response, pk:int) -> Response:
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









