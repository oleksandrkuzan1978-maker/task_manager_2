
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime

from rest_framework.views import APIView

from apps.projects.serializers import AllProjectsSerializer, ProjectDetailSerializer, CreateProjectSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from apps.tasks.models import Project
from django.http import HttpResponse

class ProjectDetailAPIView(APIView):
    def get_object(self, pk: int):
        return get_object_or_404(Project, pk=pk)

    def get(self, request: Request, pk: int):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int):
        project = self.get_object(pk=pk)
        serializer = CreateProjectSerializer(instance=project, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int) -> Response:
        project = self.get_object(pk=pk)
        project.delete()
        return Response(data={"message": "Project was deleted successfully"}
                        , status=status.HTTP_204_NO_CONTENT)






