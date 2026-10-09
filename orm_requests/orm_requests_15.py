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
from django.db.models import Q

print('\nПРАКТИКА: ЗАДАНИЕ 15\n')

# 1. Запрос с комбинацией условий с помощью Q-классов:
# (Статус 'New' И Приоритет 'Очень высокий') ИЛИ (Тег НЕ равен 'Q&A')
specific_tasks = Task.objects.filter(
    (Q(status='New') & Q(priority='Очень высокий')) | 
    ~Q(tags__name='Q&A')
).distinct()  # distinct() исключает дубликаты, если у задачи несколько тегов

# 2. Выводим требуемую по ТЗ информацию
if specific_tasks.exists():
    for task in specific_tasks:
        print("=" * 50)
        print(f"Задача: {task.title}")
        print(f"Проект: {task.project.title}")
        # Безопасный вывод email, если исполнитель не прикреплен
        if task.assignee:
            print(f"Email:  {task.assignee.email}")
        else:
            print("Email:  Исполнитель не назначен")
        print("=" * 50)
else:
    print("Задачи, соответствующие выбранной комбинации условий, не найдены.")