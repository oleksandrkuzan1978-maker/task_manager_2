import os
import sys
from pathlib import Path

import django
from django.apps import apps


def setup_django():
    """Подготовить Django для выполнения отдельных ORM-скриптов."""
    project_root = Path(__file__).resolve().parent.parent

    # Добавляем корень проекта, только если его ещё нет в путях поиска.
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Обеспечиваем корректную загрузку .env по относительному пути.
    os.chdir(project_root)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # Повторный вызов функции не требует повторной инициализации.
    if not apps.ready:
        django.setup()