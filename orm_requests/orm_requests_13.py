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

print('\nЗАДАНИЕ 13\n')

# 1. Напишите запрос, который поможет получить только те задачи, у которых:
#   ○ Статус “newˮ
#   ○ Приоритетность “Urgentˮ
from django.db.models import Q
status = 'New'
prior = 'Высокий'
# tasks = Task.objects.all()
# for task in tasks:
#     print(task.status)
#     print(task.priority)
tasks = Task.objects.filter(status=status, priority=prior)

# 2. Выведите информацию по каждой такой задаче:
#   ○ Название
#   ○ Статус
#   ○ Приоритетность
#   ○ Дата, когда задача должна быть сдана
#   ○ Email сотрудника, за которым закреплена эта задача
if tasks:
    print(f"\tЗадачи со статусом '{status}' и приоритетностью '{prior}':")
    print('\t\t',
          f"{'title':48} {'status':8} {'priority':9} {'created_at':12} {'assignee.email'}")
    print("\t\t", "-"*103)
    for task in tasks:
        print('\t\t',
              f"{task.title:48} {task.status:8} {task.priority:9} {task.created_at.date()}   {task.assignee.email}")
else:
    print(f"\tЗадачи со статусом '{status}' и приоритетностью '{prior}' не обнаружены")
