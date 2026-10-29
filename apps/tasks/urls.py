"""Маршруты просмотра задач и операций с тегами; подключение модуля задаётся корневой конфигурацией."""

from apps.tasks.views.tasks_fb import  get_all_tasks, get_put_del_tag, post_get_all_tags, get_task
from django.urls import path

urlpatterns = [
    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/<int:task_id>/', get_task, name='get_task'),
    path('tags/', post_get_all_tags, name='post_get_all_tags'),
    path('tags/<int:tag_id>/', get_put_del_tag, name='get_put_del_tag'),
    ]