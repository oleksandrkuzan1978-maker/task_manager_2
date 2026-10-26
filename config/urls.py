"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.projects.views.projects_fb import get_all_projects, index
from apps.tasks.views.tasks_fb import  get_all_tasks, get_put_del_tag, post_get_all_tags, get_task
urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('projects/', get_all_projects, name='get_all_projects'),
    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/<int:task_id>/', get_task, name='get_task'),
    path('tags/', post_get_all_tags, name='post_get_all_tags'),
    path('tags/<int:tag_id>/', get_put_del_tag, name='get_put_del_tag'),

]
