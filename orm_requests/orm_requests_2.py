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

# Задание 1 (если нужно запустить еще раз или проверить):
# tags_list = [Tag(name='Backend'), Tag(name='Frontend'), Tag(name='Q&A'), Tag(name='Design'), Tag(name='DevOPS')]
# for tag in tags_list:
#     tag.save()

# Задание 2: Создание проектов
tiger_project = Project(title='TIGER', description='THIS IS A FIRST PROJECT')
tiger_project.save()

saphyr_project = Project.objects.create(title='SapHYR INC', description='THE BEST PROJECT EVER')

print("Задание 2: Проекты 'TIGER' и 'SapHYR INC' успешно созданы!")
print(Project.objects.all())
