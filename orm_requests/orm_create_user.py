"""Создание пользователя через менеджер с проверкой существующего email."""
from getpass import getpass
# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from django.contrib.auth import get_user_model

User = get_user_model()

email = "anna@example.com"

if User.objects.filter(email=email).exists():
    print("Email already exists")
else:
    # get_user_model() возвращает модель, указанную в AUTH_USER_MODEL;
    # getpass() позволяет ввести пароль в терминале, не сохраняя его в исходном коде.
    user = User.objects.create_user(email=email
                             , password=getpass("Enter your password: ")
                             , username="anna"
                             , first_name="Anna"
                             , last_name="Ivanova")

    print(f"User created successfully: id={user.pk}, email={user.email}")
