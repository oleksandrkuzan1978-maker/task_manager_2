from datetime import timedelta
from django.utils import timezone
from django.db.models import Count

if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()
# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from apps.tasks.models import Project
# 4. Создайте переменную в которой будет храниться искомая дата проекта, например “20230707ˮ.

print('\nЗАДАНИЕ 23\n')

req_date = timezone.datetime(2026, 10, 10).astimezone()
min_files = 3
# 5. Напишите запрос, который будет фильтровать проекты по следующим параметрам:
# ○ Дата создания должна быть больше той даты, что мы получили ранее
# ○ Кол-во файлов для проекта должно быть больше, или равно переданному, например трём
projects = Project.objects.annotate(files_count=Count("files")).filter(created_at__date__gt=req_date,
                                                                       files_count__gte=min_files)
if projects.exists():
    for project in projects:
        print(f"Проект '{project.title}' создан {project.created_at.date()}, "
              f"кол-во файлов проекта: {project.files_count}")
else:
    print("Проекты, удовлетворяющие заданным условиям не найдены.")
