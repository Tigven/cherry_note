from django.contrib import admin
from notes.models import *

import json

class NoteAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'syntax', 'level', 'owner',
        'is_expanded', 'parent_node', 'note_children',
        'tags', 'content', 'is_read_only',
        'has_code_box', 'has_table', 'has_image', 'has_file',
    ]

    list_filter = ('syntax', 'is_read_only')

    def parent_node(self, instance):
        if instance.parent:
            return instance.parent.id
        return 'None'

    def note_children(self, instance):

        children = instance.children.filter(parent__id=instance.id)

        result = []
        for child in children:
            #result.append('{} | {}'.format(child.id, child.name))
            result.append(child.id)

        return json.dumps(result)

    def tags(self, instance):
        return list(instance.tags)
        note_tags = instance.tags.all()

        return json.dumps([tag.name for tag in note_tags])

class TagAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name'
    ]


admin.site.register(Note, NoteAdmin)
#admin.site.register(Tag, TagAdmin)