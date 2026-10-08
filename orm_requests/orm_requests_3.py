# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# 3. ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.setup()
from apps.tasks.models import Project, ProjectFile

# --- КОД ВЫПОЛНЕНИЯ ЗАДАНИЙ ---
print('\nЗАДАНИЕ 3\n')
# --- ЗАДАНИЕ 3. Добавление файлов к проектам ---

# 1. Сначала получаем из базы наши созданные в Задании 2 проекта
tiger_project = Project.objects.get(title='TIGER')
saphyr_project = Project.objects.get(title='SapHYR INC')

# 2. Создаем записи файлов для проекта TIGER (используем ваши поля title и file)
tiger_file_1 = ProjectFile.objects.create(title='THE FIRST FILE', file='projects/tiger/THE_first_file.doc')
tiger_file_2 = ProjectFile.objects.create(title='IMPORTANT DOCUMENT', file='projects/tiger/important_doc_9s9fh7g4hd4hgf6.pdf')
tiger_file_3 = ProjectFile.objects.create(title='README', file='projects/tiger/README.md')

# Привязываем файлы к проекту TIGER через метод .add() (ваше поле называется files)
tiger_project.files.add(tiger_file_1)
tiger_project.files.add(tiger_file_2)
tiger_project.files.add(tiger_file_3)

# 3. Создаем записи файлов для проекта SapHYR INC
saphyr_file_1 = ProjectFile.objects.create(title='README', file='projects/saphyr/README.md')
saphyr_file_2 = ProjectFile.objects.create(title='DB_DIAGRAMM', file='projects/saphyr/db_schema_h3g45f67d.drawio')
saphyr_file_3 = ProjectFile.objects.create(title='budget', file='projects/saphyr/proj_budget.xlsx')

# Привязываем файлы к проекту SapHYR INC
saphyr_project.files.add(saphyr_file_1)
saphyr_project.files.add(saphyr_file_2)
saphyr_project.files.add(saphyr_file_3)

print("Задание 3: Файлы успешно созданы и привязаны к проектам!")
print(f"Количество файлов в TIGER: {tiger_project.count_of_files}")
