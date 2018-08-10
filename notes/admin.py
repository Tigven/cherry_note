from django.contrib import admin
from notes.models import *

import json

class NoteAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'syntax',
        'is_read_only', 'parent_node', 'children',
        'tags', 'content',
        'has_code_box', 'has_table', 'has_image', 'has_file',
    ]

    list_filter = ('syntax', 'is_read_only')

    def parent_node(self, instance):
        return instance.id

    def children(self, instance):
        children = instance.children.all()

        result = []
        for child in children:
            result.append('{}|{}'.format(child.id, child.name))

        return json.dumps(result)

    def tags(self, instance):
        note_tags = instance.tags.all()

        return json.dumps([tag.name for tag in note_tags])

class TagAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name'
    ]


admin.site.register(Note, NoteAdmin)
admin.site.register(Tag, TagAdmin)