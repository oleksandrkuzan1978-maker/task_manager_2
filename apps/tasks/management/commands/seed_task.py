import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from apps.tasks.models import (Task, ProjectFile, Project, Tag)

faker = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true'
                            , help='Удалить старые данные перед заполнением')

    @transaction.atomic # если что-то упадёт, в базу не запишется ничего
    def handle(self, *args, **options):
        """Создать тестовые задачи, категории и связанные подзадачи."""
        from uuid import uuid4