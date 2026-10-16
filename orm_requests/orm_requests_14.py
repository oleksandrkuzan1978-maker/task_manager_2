# Требует доработки!
from datetime import date, timedelta

from django.db import IntegrityError
from django.utils import timezone

# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from apps.tasks.models import Task

print('\nПРАКТИКА: ЗАДАНИЕ 14\n')

title = "Update schema"
status = "Pending"
# 1. Находим запрос для конкретной задачи (берём задачу "Update schema")
task_query = Task.objects.filter(title=title)

# 2. Обновляем статс при помощи метода update()
if task_query.exists():
    try:
        updated_count = task_query.update(status=status)
        print(f"Успешно обновлено задач: {updated_count}")
    except IntegrityError as e:
        print(f"{e}: Статус {status} отсутствует в БД")

    # Проверяем результат
    updated_task = Task.objects.get(title=title)
    print(f"Новый статус задачи '{updated_task.title}: {updated_task.status}'")
else:
    print(f"задача '{title}' не найдена для обновления.")
