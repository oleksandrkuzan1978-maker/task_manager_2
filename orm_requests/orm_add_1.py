from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, F, Count, Avg, Min, Max

from django.db.models.functions import ExtractWeekDay

if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()
# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from django.contrib.auth import get_user_model
from apps.tasks.models import *

#print("_"*50)
# print('\nЗАДАНИЕ ADD_1\n')
#
# date_month_ago = timezone.now() - timedelta(days=30)
# cur_month_projects = Project.objects.filter(created_at__gte=date_month_ago)
#
# if cur_month_projects.exists():
#     for project in cur_month_projects:
#         print(f"Проект:{project.title}, Дата создания:{project.created_at.date()}")
#
# else:
#     print("EMPTY DATA")
#

#print("_"*50)
# print('\nЗАДАНИЕ ADD_2\n')
# # Словарь дней недели
# weekdays = {
#     1: 'Воскресенье',
#     2: 'Понедельник',
#     3: 'Вторник',
#     4: 'Среда',
#     5: 'Четверг',
#     6: 'Пятница',
#     7: 'Суббота',
# }
# # Выбираем день недели
# weekday = 7
# # Извлекаем день недели (в Django 2 — это Понедельник, так как 1 — Воскресенье)
# weekday_project_files = ProjectFile.objects.annotate(
#     weekday=ExtractWeekDay('created_at')
# ).filter(weekday=weekday)
# print(f'\n--- ЗАДАНИЕ 2: Файлы проектов за {weekday}-й день недели  ---')
# if weekday_project_files.exists():
#     for file_ in weekday_project_files:
#         print("=" * 50)
#         print(f"Название файла: {file_.title}")  # Ваше поле title
#         print(f"Путь к файлу:   {file_.file}")   # Ваше поле file
#         print("=" * 50)
# else:
#     print(f"Файлов за {weekdays[weekday]} не найдено")


#print("_"*50)
# print('\nЗАДАНИЕ ADD_3\n')
#
# print('\n--- ЗАДАНИЕ 3: Общее количество проектов ---')
#
# # 2. Напишите запрос, который будет считать количество всех проектов в базе данных
# count_of_projects = Project.objects.all().count()
#
# # 3. Выведите количество всех проектов в консоль
# print(f"Count of projects: {count_of_projects}")

#print("_"*50)
# print('\nЗАДАНИЕ ADD_4\n')
#
# count_files_of_project = ProjectFile.objects.values('projects__title').annotate(num_files=Count('id'))
#
# for files in count_files_of_project:
#     print(f'Проект: {files['projects__title']}, Кол-во файлов проекта: {files['num_files']}')


#print("_"*50)
# print('\nЗАДАНИЕ ADD_5\n')

# avg_tasks_of_project = Project.objects.annotate(avg_tasks=Avg('tasks__id'))
#
# for project in avg_tasks_of_project:
#     print(f"Project: {project.title}, Average Number of Tasks: {project.avg_tasks}")
#
#print("_"*50)
# print('\nЗАДАНИЕ ADD_6\n')
# User = get_user_model()
# count_of_tasks_to_user = User.objects.annotate(num_of_tasks=Count('tasks__id')).values_list('username', 'num_of_tasks')
# print(type(count_of_tasks_to_user))
# for username, count_of_tasks in count_of_tasks_to_user:
#     print(f"Developer - {username} | Count of tasks: {count_of_tasks}")

print("_"*50)
print('\nЗАДАНИЕ ADD_7\n')

all_tasks = (Task.objects.order_by('priority', 'due_date')
             .values_list('title', 'priority', 'due_date'))

for title, priority, due_date in all_tasks:
    print(f"Задача: '{title}', "
          f"Приоритет: '{priority}', "
          f"Срок выполнения: {due_date.date()}")


print("_"*50)
print('\nЗАДАНИЕ ADD_8\n')

User = get_user_model()

count_of_tasks_to_user = (User.objects.annotate(num_of_tasks=Count('tasks__id'))
                          .order_by('-num_of_tasks')
                          .values_list('username', 'num_of_tasks'))

for username, count_of_tasks in count_of_tasks_to_user:
    print(f"Developer - {username:9} | Count of tasks: {count_of_tasks}")


print("_"*50)
print('\nЗАДАНИЕ ADD_10\n')




