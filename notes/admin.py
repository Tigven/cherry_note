from django.contrib import admin
from notes.models import *

class NoteAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'syntax', 'is_read_only', 'has_code_box',
        'has_table', 'has_image', 'has_file', 'parent_node',
        'content'
    ]

    list_filter = ('syntax', 'is_read_only')

    def parent_node(self, instance):
        return instance.id

admin.site.register(Note, NoteAdmin)