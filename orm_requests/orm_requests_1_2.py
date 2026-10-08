# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()
# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set
from apps.tasks.models import Tag, Project


print("\nЗАДАНИЕ 1\n")

tag_names = ["Backend", "Frontend", "Q&A", "Design", "DevOPS"]

for name in tag_names:
    tag, created = Tag.objects.get_or_create(name=name)

    if created:
        print(f'Создан тег "{tag.name}", ID: {tag.pk}')
    else:
        print(f'Тег "{tag.name}" уже существует, ID: {tag.pk}')


print("\nЗАДАНИЕ 2\n")

projects_data = [
    ("TIGER", "THIS IS A FIRST PROJECT"),
    ("SapHYR INC", "THE FIRST PROJECT EVER"),
]

for title, description in projects_data:
    project, created = Project.objects.get_or_create(
        title=title,
        defaults={"description": description},
    )

    if created:
        print(f'Создан проект "{project.title}", ID: {project.pk}')
    else:
        print(f'Проект "{project.title}" уже существует, ID: {project.pk}')

