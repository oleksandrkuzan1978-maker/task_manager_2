import os
from datetime import date

import django


# Настройка окружения и инициализация Django для работы с ORM вне сервисного процесса сервера
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.tasks.models import Tag

tags_list = [Tag(name='Backend'), Tag(name='Frontend'),
             Tag(name='Q&A'), Tag(name='Design'), Tag(name='DevOPS')]
for tag in tags_list:
    tag.save()



