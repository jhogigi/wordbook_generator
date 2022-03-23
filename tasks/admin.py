from django.contrib import admin

from tasks.models import Task, Morph, Word


class TaskAdmin(admin.ModelAdmin):
    list_display = ('original_file_path', 'output_file_path', 'async_result_id')

class MorphAdmin(admin.ModelAdmin):
    list_display = ('wordname', 'meaning', 'parts_of_speech')

class WordAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'task', 'morph')

admin.site.register(Task, TaskAdmin)
admin.site.register(Morph, MorphAdmin)
admin.site.register(Word, WordAdmin)
