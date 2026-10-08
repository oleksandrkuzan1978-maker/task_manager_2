# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set

from apps.tasks.models import  Task, Tag

print('\nЗАДАНИЕ 6\n')

# 1. Получаем все объекты тегов и создаём словарь для поиска по имени.
tags = {tag.name: tag for tag in Tag.objects.all()}

# Указываем, какой тег соответствует названию задачи.
task_tags = {"Update new endpoint to delete panel": "Backend",
    "Update 404 page": "Frontend",}

tasks = Task.objects.filter(title__in=task_tags)
if not tasks:
    print("Таких задач не обнаружено")
for task in tasks:
    tag_name = task_tags[task.title]
    tag = tags.get(tag_name)
    if tag is None:
        print(f'Тег {tag_name} не найден')
        continue
    # 2. Обращаемся к полю tags через точку.
    # 3. Передаём объект тега методу add().
    task.tags.add(tag)

    print(f'Задаче "{task.title}" добавлен тег "{tag.name}".')





