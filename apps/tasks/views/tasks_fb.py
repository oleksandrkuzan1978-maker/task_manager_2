from django.shortcuts import get_object_or_404
from apps.tasks.serializers import TagsSerializer, AllTasksSerializer, TaskInfoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from apps.tasks.models import Task, Tag


@api_view(['GET'])
def get_all_tasks(request):
    project_title = request.query_params.get('project')
    if not project_title:
        all_tasks = Task.objects.all().order_by('id')
    else:
        all_tasks = Task.objects.filter(project__title=project_title).select_related('project').order_by('id')

    if not all_tasks.exists():
        return Response({'Tasks': 'Tasks not found'}, status=status.HTTP_204_NO_CONTENT)
    serializer = AllTasksSerializer(all_tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskInfoSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def post_get_all_tags(request):
    if request.method == 'POST':
        new_tag = TagsSerializer(data=request.data)
        if new_tag.is_valid(raise_exception=True):
            new_tag.save()
            return Response(new_tag.data, status=status.HTTP_201_CREATED)
        return Response(new_tag.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        tags = Tag.objects.all()
        if not tags.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def  get_put_del_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'GET':
        serializer = TagsSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = TagsSerializer(tag, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    if request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)