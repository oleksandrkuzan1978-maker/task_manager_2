"""Учебный поиск файлов с датой создания не ранее чем через семь дней от сегодня и связанных проектов."""

from datetime import timedelta
from django.utils import timezone

if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from apps.tasks.models import  Project, ProjectFile

print('\nЗАДАНИЕ 20\n')

# 2. Создайте переменную с датой периода создания файлов (от текущего дня -7 дней)
create_date = timezone.localdate() + timedelta(days=7)

# 3. Напишите первый запрос, который поможет получить те файлы, которые должны быть больше, или
# равны полученной дате по полю создания этого файла
files = ProjectFile.objects.filter(created_at__date__gte=create_date)
if files.exists():
    print(f"Файлы, созданные позже {create_date}:")
    for f in files:
        print("\t\t", f)
# 4. Напишите запрос, который поможет получить только те проекты, у которых есть те файлы, что мы
# получили предыдущим запросом.
# 5. Выведите информацию об этих проектах: имя проекта и дата создания.
    projects = Project.objects.filter(files__in=files).distinct()

    print(f"\nПроекты, у которых есть файлы, созданные позже {create_date}:")
    for project in set(projects):
        print("\t\t", f"Проект: {project.title}, дата создания: {project.created_at}")
else:
    print(f"Файлы, созданные позже {create_date} не обнаружены")



