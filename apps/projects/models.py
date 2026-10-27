"""Модели проектов и файлов, связанных отношением многие ко многим."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectFile(models.Model):
    """Файл с названием, путём хранения и датой создания; может принадлежать нескольким проектам."""
    title = models.CharField(max_length=120, verbose_name=_("Название файла"))
    file = models.FileField(upload_to='projects/', verbose_name=_("Файл"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    class Meta:
        """Таблица, подписи, порядок и ограничения модели ProjectFile."""
        db_table = 'project_file'
        verbose_name = _("Файл проекта")
        verbose_name_plural = _("Файлы проектов")
        ordering = ['-created_at']  # От последнего к первому

    def __str__(self):
        """Вернуть название объекта."""
        return self.title


class Project(models.Model):
    """Проект с уникальным названием, описанием, датой создания и набором файлов."""
    title = models.CharField(max_length=200, unique=True, verbose_name=_("Название проекта"))
    description = models.TextField(verbose_name=_("Описание проекта"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    files = models.ManyToManyField(ProjectFile, related_name='projects', blank=True, verbose_name=_("Файлы"))

    class Meta:
        """Таблица, подписи, порядок и ограничения модели Project."""
        db_table = 'project'
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекты")
        ordering = ['-title']  # По названию в порядке убывания
        unique_together = ('title', 'description')  # Уникальность по названию и описанию
        constraints = [models.UniqueConstraint(fields=['title',], name='unique_title')]

    def __str__(self):
        """Вернуть название объекта."""
        return self.title

    @property
    def count_of_files(self):
        """Вернуть количество файлов, связанных с этим проектом."""
        return self.files.count()