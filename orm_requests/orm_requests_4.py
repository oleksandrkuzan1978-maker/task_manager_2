# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# 3. ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.setup()


# --- КОД ВЫПОЛНЕНИЯ ЗАДАНИЙ ---
print('\nЗАДАНИЕ 4\n')
# --- ЗАДАНИЕ 4. Создание пользователей для работы в проекте ---
from django.contrib.auth.models import User

# Используем get_or_create, чтобы скрипт можно было запускать многократно без ошибок уникальности
backend, created = User.objects.get_or_create(
    username='backend',
    defaults={'email': 'backend.dev@gmail.com'}
)
if created:
    backend.set_password('sd7f6g5fsfd')
    backend.save()

frontend, created = User.objects.get_or_create(
    username='frontend',
    defaults={'email': 'frontend.dev@gmail.com'}
)
if created:
    frontend.set_password('sd7f6g5fsfd')
    frontend.save()

designer, created = User.objects.get_or_create(
    username='designer',
    defaults={'email': 'omg.designer@icloud.com'}
)
if created:
    designer.set_password('sd7f6g5fsfd')
    designer.save()

devops, created = User.objects.get_or_create(
    username='devops',
    defaults={'email': 'devops.3000@icloud.com'}
)
if created:
    devops.set_password('sd7f6g5fsfd')
    devops.save()

qa, created = User.objects.get_or_create(
    username='qa',
    defaults={'email': 'qa.doesntmetter@gmail.com'}
)
if created:
    qa.set_password('sd7f6g5fsfd')
    qa.save()

print("Задание 4: Пользователи успешно проверены/созданы в базе данных!")
print([user.username for user in User.objects.all()])
