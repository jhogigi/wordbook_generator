from django.contrib import admin

from morphogical_analyzer.models import Morph, Word


class MorphAdmin(admin.ModelAdmin):
    list_display = ('wordname', 'meaning', 'parts_of_speech')


class WordAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'task', 'morph')


admin.site.register(Morph, MorphAdmin)
admin.site.register(Word, WordAdmin)
