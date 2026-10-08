# Поддерживаем и запуск через python -m, и прямой запуск Current File.
if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# ИМПОРТЫ МОДЕЛЕЙ — СТРОГО ПОСЛЕ django.set

print('\nЗАДАНИЕ 7\n')

#1. Импортируйте модели тегов Tag.
from apps.tasks.models import  Task, Tag

# 2. Напишите запрос, который позволит получить список всех тегов.
tags = Tag.objects.all().order_by('name')

# 3. Выведите имя каждого тега.
print("\tСписок тегов:")
for tag in tags:
    print("\t\t", tag.name)

# 4. Получите самый первый тег.
# 5. Получите самый последний тег.
print(f"\tПервый тег: '{tags[0]}', \n\tПоследний тег: '{tags.last()}'")

# 6. Получите кол-во всех тегов.
print(f"\tКол-во всех тегов: {tags.count()}")

print('\nЗАДАНИЕ 8\n')

# 1. Напишите запрос, который будет искать тэг по определённому имени
# 2. Проверьте наличие такого тега методом, который выдаёт True или False на наличие объекта.
NAME_OF_TAG = 'Q&A'
tag_by_name = Tag.objects.filter(name=NAME_OF_TAG)
if tag_by_name.exists():
    print(f"\tТег по имени '{NAME_OF_TAG}' найден:")
else:
    print(f"\tТег по имени '{NAME_OF_TAG}' не обнаружен:")

print('\nЗАДАНИЕ 9\n')

# 1. Напишите запрос, который позволит получить теги, у которых в имени будет совпадение по
# переданной строке, например: “...Tagˮ
# 2. Выведите имена всех этих тегов.
ROW_MATCH = "De"
tags_by_row = Tag.objects.filter(name__icontains=ROW_MATCH)
if tags_by_row:
    print(f"\tТеги со строкой '{ROW_MATCH}' в их именах:")
    for tag in tags_by_row:
        print("\t"*5, tag.name)
else:
    print(f"Теги со строкой '{ROW_MATCH}' в их именах не обнаружены:")





