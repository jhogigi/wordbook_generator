from django.contrib import admin

from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('original_file_path', 'output_file_path', 'async_result_id')


admin.site.register(Task, TaskAdmin)
