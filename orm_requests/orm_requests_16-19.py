from datetime import date, timedelta

from django.utils import timezone

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
    print(f"Найдено задач без исполнителя: {tasks_without_assignee.count()}\n")
    for task in tasks_without_assignee:
        print("=" * 50)
        print(f"задача: {task.title}")
        print(f"Проект: {task.project.title}")
        print("=" * 50)
else:
    print("Все задачи распределены!")

print('\nПРАКТИКА: ЗАДАНИЕ 19\n')

tasks_with_qa_tags = Task.objects.filter(tags__name__icontains="Q&A").distinct()

if tasks_with_qa_tags.exists():
    for task in tasks_with_qa_tags:
        print("=" * 50)
        print(f"Имя задачи: {task.title}")
        print(f"Статус задачи: {task.status}")
        print(f"Приоритет: {task.priority}")
        print(f"Имя проекта: {task.project.title}")
        print("=" * 50)
else:
    print("Задачи с тегом 'Q&A' не найдены.")
