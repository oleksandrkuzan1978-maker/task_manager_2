from django.contrib import admin
from .models import  Project, ProjectFile
# Register your models here.

@admin.action(description="Заменить пробелы на нижние подчеркивания в названии")
def replace_spaces_with_underscores(modeladmin, request, queryset):
    for obj in queryset:
        obj.title = obj.title.replace(' ', '_')
        obj.save()
    modeladmin.message_user(request, "Пробелы успешно заменены на '_' в выбранных объектах.")


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
