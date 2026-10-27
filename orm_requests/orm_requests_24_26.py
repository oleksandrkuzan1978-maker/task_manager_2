"""Учебные запросы задач по сроку, приоритету и статусу и обновление приоритета задач TIGER.

Последнее обновление выбирает задачи, созданные раньше текущего момента, без вычитания месяца.
"""

from django.utils import timezone
import calendar
from datetime import datetime, timedelta
from django.db.models import Q, F

if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()
# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from apps.tasks.models import Task, Priority, Status

print('\nЗАДАНИЕ 24\n')

# Напишите функцию, которая будет высчитывать конец месяца от текущей даты.
def calculate_end_of_month() -> datetime:
    """Вернуть полночь последнего дня текущего по timezone.now() месяца в системном часовом поясе.

    Это начало последнего дня, а не последний момент месяца.
    """
    current_date = timezone.now()
    amount_of_days = calendar.monthrange(current_date.year, current_date.month)[1]
    date = datetime(year=current_date.year, month=current_date.month, day=amount_of_days)
    return date.astimezone()
end_of_month = calculate_end_of_month()
print(f"Конец месяца от текущей даты {end_of_month}")
# 5. Напишите запрос, который будет фильтровать задачи по нескольким условиям:
# ○ Приоритет задачи или “Criticalˮ или “Urgentˮ
# ○ Дата, когда задача должна быть закрыта(due_date) - дата конца месяца с текущей даты
tasks_filtered = Task.objects.filter(Q(priority=Priority.HIGH) | Q(priority=Priority.CRITICAL),
                                     due_date__lte=end_of_month)

if tasks_filtered.exists():
    print("Найденные задачи:")
    for task in tasks_filtered:
        print(task.title)
else:
    print("Задачи, удовлетворяющие заданным условиям не найдены.")

print('\nЗАДАНИЕ 25\n')

# Напишите запрос, который будет получать все задачи, кроме тех, что будут переданы в фильтр,
# например: “pendingˮ и “doneˮ.
tasks_excluded = Task.objects.exclude(Q(status=Status.PENDING) | Q(status=Status.DONE))
#tasks_excluded = Task.objects.filter(~(Q(status=Status.PENDING) | Q(status=Status.DONE)))
if tasks_excluded.exists():
    print("Найденные задачи:")
    for task in tasks_excluded:
        print("\t\t", task.title)
else:
    print("Задачи, удовлетворяющие заданным условиям не найдены.")

print('\nЗАДАНИЕ 26\n')

project_title = 'TIGER'
priority = Priority.CRITICAL
# 3. Создайте переменную, где будет храниться определённая дата (месяц назад относительно текущей
# даты).
one_month_ago = timezone.now() # - timedelta(days=30)
# 4. Напишите запрос, который будет получать все задачи из конкретного проекта, например “TIGERˮ,
# которые были созданы месяц назад.
# 5. Обновите приоритетность таких задач на самую высокую.
filtered_tasks = Task.objects.filter(project__title=project_title,
                    created_at__lt=one_month_ago)
if filtered_tasks.exists():
    count_filtered_tasks = filtered_tasks.count()
    count_filtered = filtered_tasks.update(priority=priority)
    if count_filtered_tasks == count_filtered:
        print(f"У {count_filtered} задач приоритетность обновлена на '{priority}'")
else:
    print("Задачи, удовлетворяющие заданным условиям не найдены.")





