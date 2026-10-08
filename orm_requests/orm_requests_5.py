import os
import sys
from pathlib import Path
import django

# 1. Настраиваем пути и модуль настроек Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# 2. Инициализируем Django (база данных и настройки подгружаются здесь)
django.setup()

# 3. ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.setup()
from apps.tasks.models import Tag, Project

# --- КОД ВЫПОЛНЕНИЯ ЗАДАНИЙ ---

# --- ЗАДАНИЕ 5. Создание задач для проектов ---
from django.utils import timezone
from datetime import timedelta
from apps.tasks.models import Task, Project
from django.contrib.auth.models import User

# 1. Получаем необходимые объекты проектов и пользователей для связей
tiger_project = Project.objects.get(title='TIGER')
saphyr_project = Project.objects.get(title='SapHYR INC')

backend_dev = User.objects.get(username='backend_dev')
frontend_dev = User.objects.get(username='frontend_dev')
designer_dev = User.objects.get(username='designer')
devops_dev = User.objects.get(username='devops')
qa_dev = User.objects.get(username='qa_dev')

# Базовая дата для дедлайнов (например, через 2 недели)
base_deadline = timezone.now() + timedelta(weeks=2)

# --- Часть 1: Задачи для проекта TIGER ---
tiger_tasks_data = [
    {"title": "Create new endpoint to get all project's tasks", "priority": "Высокий", "assignee": backend_dev},
    {"title": "Update schema", "priority": "Высокий", "assignee": backend_dev},
    {"title": "Connect new microservice", "priority": "Средний", "assignee": devops_dev},
    {"title": "Update Stage build", "priority": "Высокий", "assignee": devops_dev},
    {"title": "Update UX to mobile app", "priority": "Очень высокий", "assignee": designer_dev},
    {"title": "Update 404 page", "priority": "Высокий", "assignee": frontend_dev},
    {"title": "Test new functionality", "priority": "Очень высокий", "assignee": qa_dev},
    {"title": "test register form", "priority": "Средний", "assignee": qa_dev},
]

for t_data in tiger_tasks_data:
    Task.objects.get_or_create(
        title=t_data["title"],
        project=tiger_project,
        defaults={
            "priority": t_data["priority"],
            "assignee": t_data["assignee"],
            "due_date": base_deadline
        }
    )

# --- Часть 2: Задачи для проекта SapHYR INC ---
saphyr_tasks_data = [
    {"title": "Update new endpoint to delete panel", "priority": "Высокий", "assignee": backend_dev},
    {"title": "Update DB schema", "priority": "Высокий", "assignee": backend_dev},
    {"title": "Connect new Azure storage", "priority": "Средний", "assignee": devops_dev},
    {"title": "Update Build pipelines", "priority": "Высокий", "assignee": devops_dev},
    {"title": "Update UI to desktop app", "priority": "Очень высокий", "assignee": designer_dev},
    {"title": "Update redirect page", "priority": "Высокий", "assignee": frontend_dev},
    {"title": "Test new mobile functionality", "priority": "Очень высокий", "assignee": qa_dev},
    {"title": "test update account form", "priority": "Средний", "assignee": qa_dev},
]

for t_data in saphyr_tasks_data:
    Task.objects.get_or_create(
        title=t_data["title"],
        project=saphyr_project,
        defaults={
            "priority": t_data["priority"],
            "assignee": t_data["assignee"],
            "due_date": base_deadline
        }
    )

print("Задание 5: Все задачи для проектов 'TIGER' и 'SapHYR INC' успешно созданы!")
print(f"Общее количество задач в базе: {Task.objects.count()}")
