from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _



class ProjectFile(models.Model):
    title = models.CharField(max_length=120, verbose_name=_("Название файла"))
    file = models.FileField(upload_to='projects/', verbose_name=_("Файл"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    class Meta:
        db_table = 'project_file'
        verbose_name = _("Файл проекта")
        verbose_name_plural = _("Файлы проектов")
        ordering = ['-created_at']  # От последнего к первому

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name=_("Название проекта"))
    description = models.TextField(verbose_name=_("Описание проекта"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    files = models.ManyToManyField(ProjectFile, related_name='projects', blank=True, null=True, verbose_name=_("Файлы"))

    class Meta:
        db_table = 'project'
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекты")
        ordering = ['-title']  # По названию в порядке убывания
        unique_together = ('title', 'description')  # Уникальность по названию и описанию
        constraints = [models.UniqueConstraint(fields=['title',], name='unique_title')]

    def __str__(self):
        return self.title

    @property
    def count_of_files(self):
        """Возвращает количество файлов для конкретного объекта Project"""
        return self.files.count()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Имя тега"))

    class Meta:
        db_table = 'tag'
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")
        constraints = [models.UniqueConstraint(fields=['name',], name='unique_tag')]

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('New', _('Новая')),
        ('In progress', _('В процессе')),
        ('Pending', _('Ожидание')),
        ('Blocked', _('Заблокирована')),
        ('Done', _('Выполнено')),
    ]

    PRIORITY_CHOICES = [
        ('Низкий', _('Низкий')),
        ('Средний', _('Средний')),
        ('Высокий', _('Высокий')),
        ('Очень высокий', _('Очень высокий')),
    ]

    title = models.CharField(
        max_length=200,
        unique=True,
        validators=[MinLengthValidator(10, message="Минимальная длина названия — 10 символов.")],
        verbose_name=_("Название задачи")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='New', verbose_name=_("Статус"))
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='Средний', verbose_name=_("Приоритет"))
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
        db_table = 'task'
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")
        ordering = ['due_date', 'assignee']  # Сортировка по дедлайну (от дальней к ближней) и исполнителю
        unique_together = ('title', 'project')
        constraints = [models.UniqueConstraint(fields=['title',], name='unique_task')]

    def __str__(self):
        return self.title



