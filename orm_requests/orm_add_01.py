import os
from django.utils import timezone
from bootstrap import setup_django

setup_django()
from apps.tasks.models import Project

print('\n--- ЗАДАНИЕ 1: Проекты за текущий месяц ---')

# Фильтруем проекты по номеру текущего месяца (используем ваши поля created_at и title)
cur_month_projects = Project.objects.filter(created_at__month=timezone.now().month)

if cur_month_projects.exists():
    for proj in cur_month_projects:
        print("=" * 50)
        print(f"Проект: {proj.title}")
        print(f"Дата создания: {proj.created_at}")
        print("=" * 50)
else:
    print("EMPTY DATA")
