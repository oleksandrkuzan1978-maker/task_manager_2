"""Модели задач и тегов и перечисления допустимых статусов и приоритетов."""

from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.projects.models import Project

class Tag(models.Model):
    """Уникальный именованный тег для группировки задач."""
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Имя тега"))

    class Meta:
        """Таблица, подписи, порядок и ограничения модели Tag."""
        db_table = 'tag'
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")
        constraints = [models.UniqueConstraint(fields=['name',], name='unique_tag')]

    def __str__(self):
        """Вернуть имя тега."""
        return self.name

class Status(models.TextChoices):
    """Допустимые строковые значения статуса задачи и их русские подписи."""
    NEW = 'New', _('Новая')
    IN_PROGRESS = 'In progress', _('В процессе')
    PENDING = 'Pending', _('Ожидание')
    BLOCKED = 'Blocked', _('Заблокирована')
    DONE = 'Done', _('Выполнено')

class Priority(models.TextChoices):
    """Допустимые строковые значения приоритета задачи и их подписи."""
    LOW = 'Низкий', _('Низкий')
    MEDIUM = 'Средний', _('Средний')
    HIGH = 'Высокий', _('Высокий')
    CRITICAL = 'Очень высокий', _('Очень высокий')


class Task(models.Model):

    """Задача проекта со статусом, приоритетом, сроком, необязательным исполнителем и тегами."""
    title = models.CharField(
        max_length=200,
        unique=True,
        validators=[MinLengthValidator(10, message="Минимальная длина названия — 10 символов.")],
        verbose_name=_("Название задачи")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))
    status = models.CharField(max_length=15, choices=Status, default='New', verbose_name=_("Статус"))
    priority = models.CharField(max_length=15, choices=Priority, default='Средний', verbose_name=_("Приоритет"))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name=_("Проект"))
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True, verbose_name=_("Теги"))
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL
                                 , on_delete=models.SET_NULL
                                 , null=True, blank=True
                                 , related_name='tasks', verbose_name=_("Исполнитель"))

    due_date = models.DateTimeField(verbose_name=_("Срок выполнения (due date)"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Дата удаления"))

    class Meta:
        """Таблица, подписи, порядок и ограничения модели Task."""
        db_table = 'task'
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")
        ordering = ['due_date', 'assignee']  # Сортировка по дедлайну (от дальней к ближней) и исполнителю
        unique_together = ('title', 'project')
        constraints = [models.UniqueConstraint(fields=['title',], name='unique_task'),
                       models.CheckConstraint(condition=models.Q(status__in=Status.values)
                                              , name='task_status_valid'),
                       models.CheckConstraint(condition=models.Q(priority__in=Priority.values),
                                              name='task_priority_valid')]

    def __str__(self):
        """Вернуть название объекта."""
        return self.title



