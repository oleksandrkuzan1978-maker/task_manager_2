# Требует доработки!
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

print('\nЗА ПРАКТИКУ: ЗАДАНИЕ 14\n')

# 1. Находим запрос для конкретной задачи (берём задачу "Update schema")
task_query = Task.objects.filter(title="Update schema")

# 2. Обновляем статс при помощи метода update()
if task_query.exists():
    updated_count = task_query.update(status="Pending")
    print(f"Успешно обновлено задач: {updated_count}")

    # Проверяем результат
    updated_task = task_query.first()
    print(f"Новый статус задачи '{updated_task.title}: {updated_task.status}'")
else:
    print("задача с названием 'Update schema' не найдена для обновления.")
