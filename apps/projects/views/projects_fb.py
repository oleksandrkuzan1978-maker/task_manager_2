from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime

from apps.projects.serializers import AllProjectsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.tasks.models import Project
from django.http import HttpResponse
from rest_framework.views import APIView

"""Текстовая главная страница проекта."""
def index(request):
    """Вернуть текст главной страницы проекта."""
    return HttpResponse("Главная страница")

# Create your views here.
# @api_view(['GET'])
# def get_all_projects(request):
#     all_projects = Project.objects.all()
#     if all_projects.exists():
#         serializer = AllProjectsSerializer(all_projects, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response({'Products': 'Projects not found'}, status=status.HTTP_204_NO_CONTENT)


##Закончили на Задании 7 (Adpractice_Pr5, стр. 43-44)


class ProjectView(APIView):
    def get_all_projects(self, date_from=None, date_to=None):
        if date_from and date_to:
            date_from = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
            date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d')) \
                if date_from else timezone.now().strftime('%Y-%m-%d')

        all_projects = Project.objects.all()
        if all_projects.exists():
            serializer = AllProjectsSerializer(all_projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Products': 'Projects not found'}, status=status.HTTP_204_NO_CONTENT)




