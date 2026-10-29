"""Настройки административной панели для проектов и файлов и действие переименования проектов."""

from django.contrib import admin
from .models import  Project, ProjectFile
# Register your models here.

@admin.action(description="Заменить пробелы на нижние подчеркивания в названии")
def replace_spaces_with_underscores(modeladmin, request, queryset):
    """Заменить пробелы на подчёркивания в названиях выбранных объектов и сообщить результат."""
    for obj in queryset:
        obj.title = obj.title.replace(' ', '_')
        obj.save()
    modeladmin.message_user(request, "Пробелы успешно заменены на '_' в выбранных объектах.")


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    """Показ названия, пути и даты файла с поиском по названию и фильтром по дате."""
    list_display = ('title', 'file', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Показ проектов с количеством файлов, поиском по названию и действием замены пробелов."""
    list_display = ('title', 'created_at', 'count_of_files_display')
    search_fields = ('title',)
    actions = [replace_spaces_with_underscores]

    def count_of_files_display(self, obj):
        """Вернуть количество связанных файлов для колонки административной панели."""
        return obj.count_of_files
    count_of_files_display.short_description = "count of Files"  # Название колонки в админке
