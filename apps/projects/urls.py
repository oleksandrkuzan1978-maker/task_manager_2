"""Маршрут списка файлов и загрузки файла в проект."""

from apps.projects.views.project_file_views import ProjectFileListAPIView
from apps.projects.views.projects_cls import ProjectDetailAPIView
from apps.projects.views.projects_fb import get_all_create_projects, get_patch_delete_project
from django.urls import path
urlpatterns = [
    path('files/', ProjectFileListAPIView.as_view(), name='files-list'),
    path('projects/', get_all_create_projects, name='get_all_create_projects'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='get_put_delete_project'),


]
