from django.shortcuts import get_object_or_404

from apps.serializers.projects import AllProjectsSerializer
from apps.serializers.tags import TagsSerializer
from apps.serializers.tasks import AllTasksSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from apps.tasks.models import Project, Task, Tag

# Create your views here.
@api_view(['GET'])
def get_all_projects(request):
    all_projects = Project.objects.all()
    if all_projects.exists():
        serializer = AllProjectsSerializer(all_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'Products': 'Projects not found'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_all_tasks(request):
    project_title = request.query_params.get('project')
    if not project_title:
        all_tasks = Task.objects.all().order_by('id')
    else:
        all_tasks = Task.objects.filter(project__title=project_title).order_by('id')

    if not all_tasks.exists():
        return Response({'Tasks': 'Tasks not found'}, status=status.HTTP_204_NO_CONTENT)
    serializer = AllTasksSerializer(all_tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_tags(request):
    tags = Tag.objects.all()
    if not tags.exists():
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = TagsSerializer(tags, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def  get_tag_by_id(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    serializer = TagsSerializer(tag)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Далее Задание 17 в Практик_4

