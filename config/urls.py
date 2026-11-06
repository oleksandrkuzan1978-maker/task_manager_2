"""Корневые маршруты главной страницы, административной панели и API проектов, файлов, задач и тегов."""
from django.contrib import admin
from django.urls import path, include
from site_index import index
from apps.users.views.users import UserListGenericView
urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('', include('apps.projects.urls')),
    path('', include('apps.tasks.urls')),
    path('users/', UserListGenericView.as_view(), name='user_list'),
]
