"""Административная панель задач и тегов с действиями изменения статуса и приоритета."""

from django.contrib import admin
from .models import Task, Tag

# --- Кастомные Админ-действия ---

@admin.action(description="Установить статус 'Выполнено'")
def set_status_done(modeladmin, request, queryset):
    """Установить выбранным задачам статус Done и сообщить количество обновлённых записей."""
    updated = queryset.update(status='Done')
    modeladmin.message_user(request, f"Статус изменен на 'Выполнено' для {updated} задач.")


@admin.action(description="Приоритет: Низкий")
def set_priority_low(modeladmin, request, queryset):
    """Массово установить выбранным задачам приоритет «Низкий»."""
    queryset.update(priority='Низкий')

@admin.action(description="Приоритет: Средний")
def set_priority_medium(modeladmin, request, queryset):
    """Массово установить выбранным задачам приоритет «Средний»."""
    queryset.update(priority='Средний')

@admin.action(description="Приоритет: Высокий")
def set_priority_high(modeladmin, request, queryset):
    """Массово установить выбранным задачам приоритет «Высокий»."""
    queryset.update(priority='Высокий')

@admin.action(description="Приоритет: Очень высокий")
def set_priority_very_high(modeladmin, request, queryset):
    """Массово установить выбранным задачам приоритет «Очень высокий»."""
    queryset.update(priority='Очень высокий')


# --- Регистрация классов ---
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Список тегов с поиском по имени."""
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Список задач с фильтрами, выбором тегов и действиями изменения статуса и приоритета."""
    list_display = ('title', 'project', 'status', 'priority', 'created_at', 'due_date', 'assignee')
    list_filter = ('status', 'priority', 'project', 'created_at', 'due_date', 'assignee')
    search_fields = ('title',)
    filter_horizontal = ('tags',)
    actions = [set_status_done, set_priority_low, set_priority_medium, set_priority_high, set_priority_very_high]
