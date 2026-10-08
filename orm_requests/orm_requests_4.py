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

# --- ЗАДАНИЕ 4. Создание пользователей для работы в проекте ---
from django.contrib.auth.models import User

# Используем get_or_create, чтобы скрипт можно было запускать многократно без ошибок уникальности
backend_dev, created = User.objects.get_or_create(
    username='backend_dev',
    defaults={'email': 'backend.dev@gmail.com'}
)
if created:
    backend_dev.set_password('sd7f6g5fsfd')
    backend_dev.save()

frontend_dev, created = User.objects.get_or_create(
    username='frontend_dev',
    defaults={'email': 'frontend.dev@gmail.com'}
)
if created:
    frontend_dev.set_password('sd7f6g5fsfd')
    frontend_dev.save()

designer_dev, created = User.objects.get_or_create(
    username='designer',
    defaults={'email': 'omg.designer@icloud.com'}
)
if created:
    designer_dev.set_password('sd7f6g5fsfd')
    designer_dev.save()

devops_dev, created = User.objects.get_or_create(
    username='devops',
    defaults={'email': 'devops.3000@icloud.com'}
)
if created:
    devops_dev.set_password('sd7f6g5fsfd')
    devops_dev.save()

qa_dev, created = User.objects.get_or_create(
    username='qa_dev',
    defaults={'email': 'qa.doesntmetter@gmail.com'}
)
if created:
    qa_dev.set_password('sd7f6g5fsfd')
    qa_dev.save()

print("Задание 4: Пользователи успешно проверены/созданы в базе данных!")
print([user.username for user in User.objects.all()])
