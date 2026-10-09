from datetime import date, timedelta

from django.utils import timezone
# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set

print('\nЗАДАНИЕ 10\n')

# 1. Импортируйте модуль datetime и модель Project.
from apps.tasks.models import  Project, ProjectFile

# 2. Создайте объект даты, по которой нужно сделать поиск.
created_at = date(2026, 10, 8)

# 3. Напишите запрос, который позволит получить список проектов, которые равны или старше
# переданной даты создания.
projects = Project.objects.filter(created_at__date__lte=created_at)

# 4. Выведите имена таких проектов.
if projects:
    print(f"Проекты, созданные не позднее даты: {created_at}")
    for project in projects:
        print("\t", project.title)
else:
    print(f"Проекты, созданные не позднее даты: {created_at} не найдены")


print('\nЗАДАНИЕ 11\n')

from django.db.models import Q
# 2. Напишите запрос, который позволит получить необходимые проекты:
#   ○ Реализуйте фильтрацию, которая будет проходить два условия:
#       ■ Проекты, равные или больше указанной даты
#       ■ Проекты, у которых в имени есть строка ‘TIʼ
created_at = date(2026, 10, 8)
row_in_title = 'TI'
specifying_projects = Project.objects.filter(Q(created_at__date__gte=created_at) & Q(title__icontains=row_in_title))

# 3. Выведите имена таких проектов.
if specifying_projects:
    print(f"Проекты, созданные позднее даты: {created_at - timedelta(days=1)}"
          f" и имеющие в своем названии '{row_in_title}':")
    for project in specifying_projects:
        print(f"\t", project.title)
else:
    print(f"Проекты, созданные позднее даты: {created_at - timedelta(days=1)}"
          f" и имеющие в своем названии '{row_in_title}' не обнаружены")

print('\nЗАДАНИЕ 12\n')

# 1. Напишите запрос, который позволит получить список всех файлов, которые привязаны к
# конкретному проекту. Поиск произведите по имени проекта.
title = 'TIGER'
required_files = ProjectFile.objects.filter(projects__title__icontains=title)

# 2. Выведите только пути к каждому файлу.
if required_files:
    print(f"Пути к файлам проекта '{title}':")
    for file in required_files:
        print(f"\t", file.file)
else:
    print(f"Не обнаружены файлы проекта '{title}'")





