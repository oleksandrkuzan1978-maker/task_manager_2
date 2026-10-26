import os
from pathlib import Path
ALLOWED_EXTENSIONS = ['.csv', '.doc', '.pdf', '.xlsx', '.py']

# Остановились на выполнении Задания 9 стр. 56


# Функция на проверку валидных расширений файла
def check_extension(filename):
    extension = Path(filename).suffix
    if extension not in ALLOWED_EXTENSIONS:
        return False
    return True

# ● Функция на проверку размерности файла (файл не должен быть больше 2 MB)
def check_file_size(file, required_size=2):
    # Переводим в Мегабайты
    file_size = file.size / (1024 * 1024)
    if file_size > required_size:
        return False
    return True

# ● Функция на создание пути для сохранения файла
def create_file_path(file_name):
    new_file_name, file_ext = file_name.split('.')

    file_path = "documents/{}.{}".format(
        new_file_name,
        file_ext
    )

    return file_path

# ● Функция на сохранение файла (файл должен записываться по частям для избежания
# потенциальных ошибок и потери данных)

def save_file(file_path, file_content):
    # Извлекаем путь к папке (documents/) и создаем её, если она еще не существует
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    # Открываем файл на запись в бинарном режиме ('wb')
    with open(file_path, 'wb') as f:
        # Метод .chunks() читает файл порциями, избегая перегрузки оперативной памяти
        for chunk in file_content.chunks():
            f.write(chunk)

    return file_path

