from django.db.models.functions import ExtractWeekDay
from bootstrap import setup_django

setup_django()
from apps.tasks.models import ProjectFile

print(f'\n--- ЗАДАНИЕ 2: Файлы проектов в день недели {weekday} ---')

# Извлекаем день недели (в Django 2 — это Понедельник, так как 1 — Воскресенье)
weekday_project_files = ProjectFile.objects.annotate(
    weekday=ExtractWeekDay('created_at')
).filter(weekday=6)

if weekday_project_files.exists():
    for file_ in weekday_project_files:
        print("=" * 50)
        print(f"Название файла: {file_.title}")  # Ваше поле title
        print(f"Путь к файлу:   {file_.file}")   # Ваше поле file
        print("=" * 50)
else:
    print(f"Файлов за {weekday} не найдено")
