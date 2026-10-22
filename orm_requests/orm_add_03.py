if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# 1. Импортируйте модель Project
from apps.tasks.models import Project

print('\n--- ЗАДАНИЕ 3: Общее количество проектов ---')

# 2. Напишите запрос, который будет считать количество всех проектов в базе данных
count_of_projects = Project.objects.all().count()

# 3. Выведите количество всех проектов в консоль
print(f"Count of projects: {count_of_projects}")
