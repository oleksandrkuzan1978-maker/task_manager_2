from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import F
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()
# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from apps.tasks.models import Task, Status

print('\nЗАДАНИЕ 21\n')

status = Status.NEW
# 2. Напишите запрос, который отфильтрует задачи по определённому статусу (‘newʼ).
tasks_to_update = Task.objects.filter(status=status)
if tasks_to_update.exists():
    print(f"Задачи со статусом {status}:")
    for task in tasks_to_update:
        print(task)
        # 3. Для всех полученных задач обновите поле status на новое значение ‘in_progressʼ.
        task.status = Status.IN_PROGRESS
    # 4. У модели вызовите метод, который позволит массово применить обновления.
    Task.objects.bulk_update(tasks_to_update, ['status'])
    # 5. Посмотрите результат, выведите поле статуса у всех задач.
    all_tasks = Task.objects.all()
    for task in all_tasks:
        print(task.status, end=', ')
else:
    print(f"Задачи со статусом {status} не обнаружены:")

print('\nЗАДАНИЕ 22\n')

status = Status.IN_PROGRESS
# 3. Получите список задач со статусом ‘in_progressʼ.
tasks_to_update = Task.objects.filter(status=status)

# 4. Для каждого полученного объекта измените дату для завершения задачи, увеличив её на 3 дня от
# той даты, что в задаче указана.
if tasks_to_update.exists():
    for task in tasks_to_update:
        task.due_date = F('due_date') + timedelta(days=3)
        # 5. У модели Task вызовите метод, который поможет массово обновить данные.
    Task.objects.bulk_update(tasks_to_update, ['due_date'])

    print(f"Срок выполнения задач со статусом '{status}' "
          f"установлен на {Task.objects.filter(status=status).first().due_date.date()}:")
else:
    print(f"Задачи со статусом {status} не обнаружены:")