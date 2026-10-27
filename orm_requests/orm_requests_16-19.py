"""Учебный скрипт изменения приоритетов и сроков задач и поиска задач по исполнителю и тегу.

При импорте также выполняет orm_requests_6 и назначает теги; срок всех задач увеличивает на неделю.
"""

from datetime import date, timedelta

from django.utils import timezone

from orm_requests.orm_requests_6 import tag_name

# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set

from apps.tasks.models import Task
from django.db.models import F

print('\nПРАКТИКА: ЗАДАНИЕ 16\n')

updated_count = Task.objects.filter(
    due_date__month=F('created_at__month') + 1
).update(priority="Очень высокий")

print(f"Приоритет успешно обновлён для {updated_count} задач(и).")

print('\nПРАКТИКА: ЗАДАНИЕ 17\n')

updated_task_count = Task.objects.update(
    due_date=F('due_date') + timedelta(weeks=1)
)

print(f"Задание 17: Срок выполнения (due_date) успешно увеличен на 1 неделю для {updated_task_count} задач(и).")

print('\nПРАКТИКА: ЗАДАНИЕ 18\n')

tasks_without_assignee = Task.objects.filter(
    assignee__isnull=True
)

if tasks_without_assignee.exists():
    print(f"Найдено {tasks_without_assignee.count()} задач без исполнителя\n")
    for task in tasks_without_assignee:
        print("=" * 50)
        print(f"задача: {task.title}")
        print(f"Проект: {task.project.title}")
        print("=" * 50)
else:
    print("Все задачи распределены!")

print('\nПРАКТИКА: ЗАДАНИЕ 19\n')

tag_name = "Q&A"

tasks_with_tag = Task.objects.filter(tags__name__icontains=tag_name).distinct()

if tasks_with_tag.exists():
    for task in tasks_with_tag:
        print("=" * 50)
        print(f"Имя задачи: {task.title}")
        print(f"Статус задачи: {task.status}")
        print(f"Приоритет: {task.priority}")
        print(f"Имя проекта: {task.project.title}")
        print("=" * 50)
else:
    print(f"Задачи с тегом '{tag_name}' не найдены.")
