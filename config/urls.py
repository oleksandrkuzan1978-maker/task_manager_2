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
from apps.tasks.views import get_all_projects, get_all_tasks, get_tag_by_id
urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', get_all_projects, name='get_all_projects'),
    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tags/<int:tag_id>/', get_tag_by_id, name='get_tag_by_id'),

]
