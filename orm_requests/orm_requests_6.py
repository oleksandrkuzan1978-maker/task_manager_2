import os
import sys
from pathlib import Path
import django

# 1. Настраиваем пути и модуль настроек Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# 2. Инициализируем Django (база данных и настройки подгружаются здесь)
django.setup()

# 3. ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.setup()
from apps.tasks.models import Tag, Project

# --- КОД ВЫПОЛНЕНИЯ ЗАДАНИЙ ---

# --- ЗАДАНИЕ 6. Добавление тэгов для всех задач ---
from apps.tasks.models import Tag, Task

# 1. Получаем объекты всех тегов из базы данных
back_tag = Tag.objects.get(name='Backend')
front_tag = Tag.objects.get(name='Frontend')
qa_tag = Tag.objects.get(name='Q&A')
design_tag = Tag.objects.get(name='Design')
devops_tag = Tag.objects.get(name='DevOPS')

# 2. Маппинг: Название задачи -> Список необходимых тегов
task_tags_map = {
    # Проект TIGER
    "Create new endpoint to get all project's tasks": [back_tag],
    "Update schema": [back_tag],
    "Connect new microservice": [devops_tag],
    "Update Stage build": [devops_tag],
    "Update UX to mobile app": [design_tag],
    "Update 404 page": [front_tag],
    "Test new functionality": [qa_tag],
    "test register form": [qa_tag],

    # Проект SapHYR INC
    "Update new endpoint to delete panel": [back_tag],
    "Update DB schema": [back_tag],
    "Connect new Azure storage": [devops_tag, front_tag],  # Пример комбинации по ТЗ (на слайде был front_tag)
    "Update Build pipelines": [devops_tag, front_tag],
    "Update UI to desktop app": [design_tag],
    "Update redirect page": [design_tag],  # Соответствует слайду решения
    "Test new mobile functionality": [qa_tag],
    "test update account form": [qa_tag],
}

# 3. Проходим по маппингу, ищем задачи в базе и привязываем теги через .add()
for task_title, tags in task_tags_map.items():
    try:
        # Так как title уникален, получаем конкретную задачу
        task_obj = Task.objects.get(title=task_title)
        # Распаковываем список тегов и добавляем их в ManyToMany поле tags
        task_obj.tags.add(*tags)
    except Task.DoesNotExist:
        print(f"Предупреждение: Задача '{task_title}' не найдена в базе данных.")

print("Задание 6: Теги успешно распределены и добавлены ко всем задачам!")
