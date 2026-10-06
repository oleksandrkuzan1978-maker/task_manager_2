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
        """Создать проекты с файлами и случайными задачами и тегами."""
        from uuid import uuid4

        from django.contrib.auth import get_user_model
        from django.core.files.base import ContentFile

        # Хранилище файлов не участвует в транзакциях базы данных.
        # Запоминаем новые файлы, чтобы убрать их при ошибке заполнения.
        saved_files = []
        try:
            if options.get('clear', False):
                self.clear()

            tags = [
                Tag.objects.get_or_create(name=name)[0]
                for name in ('Backend', 'Frontend', 'Тестирование', 'Документация',
                             'Ошибка', 'Улучшение', 'Срочно', 'Исследование')
            ]
            # Пользователей не создаём и не меняем; исполнитель необязателен.
            assignee_ids = list(
                get_user_model().objects.filter(is_active=True)
                .values_list('pk', flat=True)
            )
            statuses = [value for value, _ in Task.STATUS_CHOICES]
            priorities = [value for value, _ in Task.PRIORITY_CHOICES]
            now = timezone.now()
            project_count = 5
            task_count = 0
            file_count = 0

            for number in range(1, project_count + 1):
                # UUID сохраняет уникальность названий при повторных запусках.
                project = Project(
                    title=f'Тестовый проект {number}: {uuid4().hex}',
                    description=faker.paragraph(nb_sentences=5),
                )
                # save() не запускает валидацию модели автоматически.
                project.full_clean()
                project.save()

                for file_number in range(1, random.randint(1, 3) + 1):
                    attachment = ProjectFile(
                        title=f'Документ {file_number} проекта {number}',
                    )
                    content = f'{project.title}\n\n{faker.text(max_nb_chars=1000)}\n'
                    attachment.file.save(
                        f'seed_task_{uuid4().hex}.txt',
                        ContentFile(content.encode('utf-8')),
                        save=False,
                    )
                    saved_files.append((attachment.file.storage, attachment.file.name))
                    attachment.full_clean()
                    attachment.save()
                    # ManyToMany заполняется после сохранения обеих записей.
                    project.files.add(attachment)
                    file_count += 1

                for task_number in range(1, random.randint(5, 10) + 1):
                    task = Task(
                        title=f'Задача {number}.{task_number}: {uuid4().hex}',
                        description=faker.paragraph(nb_sentences=3),
                        project=project,
                        status=random.choice(statuses),
                        priority=random.choice(priorities),
                        assignee_id=random.choice([None, *assignee_ids]),
                        # Добавляем и просроченные задачи для проверки фильтров.
                        due_date=now + timedelta(
                            days=random.randint(-14, 45),
                            hours=random.randint(0, 23),
                        ),
                    )
                    task.full_clean()
                    task.save()
                    task.tags.set(random.sample(tags, k=random.randint(0, 4)))
                    task_count += 1

            message = (
                f'Создано проектов: {project_count}, файлов: {file_count}, '
                f'задач: {task_count}. Использовано тегов: {len(tags)}.'
            )
            transaction.on_commit(
                lambda: self.stdout.write(self.style.SUCCESS(message))
            )
        except Exception:
            # База откатится декоратором atomic; файлы удаляем отдельно.
            for storage, name in saved_files:
                try:
                    storage.delete(name)
                except Exception as error:
                    self.stderr.write(f'Не удалось удалить файл {name}: {error}')
            raise

    @transaction.atomic
    def clear(self):
        """Удалить все проекты, задачи, теги и вложения, сохранив пользователей."""
        storage = ProjectFile._meta.get_field('file').storage
        file_names = set(
            ProjectFile.objects.exclude(file='').values_list('file', flat=True)
        )
        # Задачи и промежуточные ManyToMany-связи удалятся каскадно.
        Project.objects.all().delete()
        ProjectFile.objects.all().delete()
        Tag.objects.all().delete()

        def delete_files():
            # При откате БД старые вложения должны оставаться доступными.
            for name in file_names:
                try:
                    # Не удаляем файл, если к моменту commit его снова используют.
                    if not ProjectFile.objects.filter(file=name).exists():
                        storage.delete(name)
                except Exception as error:
                    self.stderr.write(f'Не удалось удалить файл {name}: {error}')

        transaction.on_commit(delete_files, robust=True)
