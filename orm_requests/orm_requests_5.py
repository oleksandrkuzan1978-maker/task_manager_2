# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.setup()

print('\nЗАДАНИЕ 5\n')

# --- КОД ВЫПОЛНЕНИЯ ЗАДАНИЙ ---

# --- ЗАДАНИЕ 5. Создание задач для проектов ---
from django.utils import timezone
from datetime import timedelta
from apps.tasks.models import Task, Project
from django.contrib.auth.models import User

# 1. Получаем необходимые объекты проектов и пользователей для связей
tiger_project = Project.objects.get(title='TIGER')
saphyr_project = Project.objects.get(title='SapHYR INC')

backend = User.objects.get(username='backend')
frontend = User.objects.get(username='frontend')
designer = User.objects.get(username='designer')
devops = User.objects.get(username='devops')
qa = User.objects.get(username='qa')

# Базовая дата для дедлайнов (например, через 2 недели)
base_deadline = timezone.now() + timedelta(weeks=2)

# --- Часть 1: Задачи для проекта TIGER ---
tiger_tasks_data = [
    {"title": "Create new endpoint to get all project's tasks", "priority": "Высокий", "assignee": backend},
    {"title": "Update schema", "priority": "Высокий", "assignee": backend},
    {"title": "Connect new microservice", "priority": "Средний", "assignee": devops},
    {"title": "Update Stage build", "priority": "Высокий", "assignee": devops},
    {"title": "Update UX to mobile app", "priority": "Очень высокий", "assignee": designer},
    {"title": "Update 404 page", "priority": "Высокий", "assignee": frontend},
    {"title": "Test new functionality", "priority": "Очень высокий", "assignee": qa},
    {"title": "test register form", "priority": "Средний", "assignee": qa},
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
    {"title": "Update new endpoint to delete panel", "priority": "Высокий", "assignee": backend},
    {"title": "Update DB schema", "priority": "Высокий", "assignee": backend},
    {"title": "Connect new Azure storage", "priority": "Средний", "assignee": devops},
    {"title": "Update Build pipelines", "priority": "Высокий", "assignee": devops},
    {"title": "Update UI to desktop app", "priority": "Очень высокий", "assignee": designer},
    {"title": "Update redirect page", "priority": "Высокий", "assignee": frontend},
    {"title": "Test new mobile functionality", "priority": "Очень высокий", "assignee": qa},
    {"title": "test update account form", "priority": "Средний", "assignee": qa},
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
