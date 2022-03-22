from django.contrib import admin

from tasks.models import Task, Morph


class TaskAdmin(admin.ModelAdmin):
    list_display = ('original_file_path', 'output_file_path', 'async_result_id')

class MorphAdmin(admin.ModelAdmin):
    list_display = ('wordname', 'meaning', 'parts_of_speech', 'frequency', 'task')

admin.site.register(Task, TaskAdmin)
admin.site.register(Morph, MorphAdmin)
