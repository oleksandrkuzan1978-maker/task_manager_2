from django.contrib import admin, messages
from .models import Project, Task, Tag, ProjectFile

# --- Кастомные Админ-действия ---

@admin.action(description="Заменить пробелы на нижние подчеркивания в названии")
def replace_spaces_with_underscores(modeladmin, request, queryset):
    for obj in queryset:
        obj.title = obj.title.replace(' ', '_')
        obj.save()
    modeladmin.message_user(request, "Пробелы успешно заменены на '_' в выбранных объектах.")


@admin.action(description="Установить статус 'Выполнено'")
def set_status_done(modeladmin, request, queryset):
    updated = queryset.update(status='Done')
    modeladmin.message_user(request, f"Статус изменен на 'Выполнено' для {updated} задач.")


@admin.action(description="Приоритет: Низкий")
def set_priority_low(modeladmin, request, queryset):
    queryset.update(priority='Низкий')

@admin.action(description="Приоритет: Средний")
def set_priority_medium(modeladmin, request, queryset):
    queryset.update(priority='Средний')

@admin.action(description="Приоритет: Высокий")
def set_priority_high(modeladmin, request, queryset):
    queryset.update(priority='Высокий')

@admin.action(description="Приоритет: Очень высокий")
def set_priority_very_high(modeladmin, request, queryset):
    queryset.update(priority='Очень высокий')


# --- Регистрация классов ---

@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'count_of_files_display')
    search_fields = ('title',)
    actions = [replace_spaces_with_underscores]

    def count_of_files_display(self, obj):
        return obj.count_of_files
    count_of_files_display.short_description = "count of Files"  # Название колонки в админке


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'created_at', 'due_date', 'assignee')
    list_filter = ('status', 'priority', 'project', 'created_at', 'due_date', 'assignee')
    search_fields = ('title',)
    filter_horizontal = ('tags',)
    actions = [set_status_done, set_priority_low, set_priority_medium, set_priority_high, set_priority_very_high]
