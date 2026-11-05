from django.utils import timezone
import calendar
from datetime import datetime, timedelta
from django.db.models import Q, F

if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()
# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from apps.tasks.models import Task, Priority, Status, Project

date_month_ago = timezone.now() - timedelta(days=30)
cur_month_projects = Project.objects.filter(created_at__gte=date_month_ago)

if cur_month_projects.exists():
    for project in cur_month_projects:
        print(f'proj{project.title} {project.created_at.date()}')







