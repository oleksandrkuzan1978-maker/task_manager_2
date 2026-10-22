if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# 1. Импортируйте класс Avg и модель Project
from django.db.models import Avg
from apps.tasks.models import Project

print('\n--- ЗАДАНИЕ 5: Среднее количество задач на каждом проекте ---')

# 3. Напишите запрос, который для каждого проекта выведет среднее количество задач
# Используем метод annotate() для добавления вычисляемого поля avg_tasks к каждому проекту
average_project_tasks = Project.objects.annotate(avg_tasks=Avg('tasks__id'))

# 4. Выведите полученные данные
for project in average_project_tasks:
    # Заменяем project.name на ваше поле project.title
    print(f"Project: {project.title}, Average Number of Tasks: {project.avg_tasks}")
