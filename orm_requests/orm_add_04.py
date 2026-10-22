from django.db.models import Count
from bootstrap import setup_django

setup_django()
from apps.tasks.models import Project

print('\n--- ЗАДАНИЕ 4: Количество файлов для каждого проекта ---')

# Подсчитываем файлы для каждого проекта через annotate (используем ваше ManyToMany поле 'files')
projects_with_counts = Project.objects.annotate(num_files=Count('files'))

for project in projects_with_counts:
    print(f"Project: {project.title}, Number of files: {project.num_files}")
