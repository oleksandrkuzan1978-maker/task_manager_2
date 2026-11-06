"""Маршрут списка файлов и загрузки файла в проект."""

from apps.projects.views.project_file_views import (ProjectFileListAPIView
                                                    , ProjectFileListGenericView
                                                    , ProjectFileDetailGenericView
                                                    , DownloadProjectFileView)

from apps.projects.views.projects_cls import ProjectDetailAPIView
from apps.projects.views.projects_fb import get_all_create_projects, get_patch_delete_project
from django.urls import path
urlpatterns = [
    path('files/', ProjectFileListGenericView.as_view(), name='files-list'),
    path('files/<int:pk>/', ProjectFileDetailGenericView.as_view(), name='file-detail'),
    path('files/download/<int:pk>/', DownloadProjectFileView.as_view(), name='download-file'),
    path('projects/', get_all_create_projects, name='get_all_create_projects'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='get_put_delete_project'),



]
