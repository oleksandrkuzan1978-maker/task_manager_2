import os
from pathlib import Path
ALLOWED_EXTENSIONS = ['.csv', '.doc', '.pdf', '.xlsx', '.py']

# Остановились на выполнении Задания 9 стр. 56



# ● Функция на создание пути для сохранения файла
# ● Функция на сохранение файла (файл должен записываться по частям для избежания
# потенциальных ошибок и потери данных)


# Функция на проверку валидных расширений файла
def check_extension(filename):
    extension = Path(filename).suffix
    if extension not in ALLOWED_EXTENSIONS:
        return False
    return True

# ● Функция на проверку размерности файла (файл не должен быть больше 2 MB)
def check_file_size(file, required_size):
    pass

