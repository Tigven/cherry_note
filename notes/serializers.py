from django.utils import timezone
from rest_framework import serializers
from rest_framework.reverse import reverse

from notes.models import Note, Tag, File
from cherry_note.users.serializers import UserSerializer

import json

class NoteChildrenHyperlink(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        url = reverse(
            viewname='note-children', args=[obj.pk.instance.id],
            request=request, format=format
        )
        return url

class NoteChildrenField(serializers.HyperlinkedRelatedField):
    """
    Note's children (URL to resource or list of children if
    `is_expanded` filed of note is set to True)
    """
    def get_attribute(self, obj):
        return obj

    def to_representation(self, obj):
        children = obj.children.filter(parent__id=obj.id)
        serializer = PartialNoteSerializer(
            children, many=True, read_only=True
        )
        return serializer.data

        if obj.is_expanded:
            children = obj.children.filter(parent__id=obj.id)
            serializer = PartialNoteSerializer(
                children, many=True, read_only=True
            )
            return serializer.data
        elif obj.children.count():
            return list()
        else:
            return None

class NoteTagsHyperlink(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        url = reverse(
            viewname='note-tags', args=[obj.pk.instance.id],
            request=request, format=format
        )
        return url

class TagsListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        tags = data[0]
        return list(tags)
        return json.dumps(list(tags), default=str)

    def to_internal_value(self, data):
        return json.loads(data)

"""
class NoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'name', 'is_read_only',)
"""

class FileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('owner', 'name', 'size', 'url', 'info')

class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class NoteIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id',)

class PartialNoteSerializer(serializers.ModelSerializer):
    children = NoteChildrenField(
        view_name='note-children',
        read_only=True,
    )
    parent = NoteIDSerializer()
    
    class Meta:
        model = Note
        fields = (
            'id', 'name', 'syntax', 'level', 'children', 'parent',
            'is_expanded', 'tags', 'is_read_only',
            'has_code_box', 'has_table', 'has_image', 'has_file',
        )

class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True, allow_blank=True,
        max_length=100
    )
    content = serializers.CharField(required=False)
    syntax = serializers.ChoiceField(
        choices=Note.SYNTAX_CHOICES,
        default='simple'
    )
    has_code_box = serializers.BooleanField(required=False)
    has_table = serializers.BooleanField(required=False)
    has_image = serializers.BooleanField(required=False)
    has_file = serializers.BooleanField(required=False)
    level = serializers.IntegerField(required=False)
    ts_created = serializers.DateTimeField(read_only=True)
    ts_updated = serializers.DateTimeField(read_only=True)
    is_read_only = serializers.BooleanField(required=False)
    is_expanded = serializers.BooleanField(required=False)

    #owner = serializers.HyperlinkedRelatedField(
    #    view_name='user-detail',
    #    read_only=True,
    #)
    owner = UserSerializer(read_only=True)
    parent = NoteIDSerializer()
    #parent = serializers.HyperlinkedRelatedField(
    #    view_name='note-detail',
    #    queryset=Note.objects.all()[:30],
    #    required=False,
    #)
    #tags = NoteTagsHyperlink(
    #    view_name='note-tags',
    #    read_only=True,
    #)
    #tags = TagModelSerializer(
    #    many=True, #read_only=True,
    #    #queryset=Tag.objects.all(),
    #)
    #tags = TagsListField(
    #    required=False,
    #)
    tags = serializers.JSONField(required=False)
    #children = NoteChildrenHyperlink(
    #    view_name='note-children',
    #    read_only=True,
    #)
    children = NoteChildrenField(
        view_name='note-children',
        read_only=True,
    )

    def create(self, validated_data):
        """
        Create and return a new `Note` instance, given the validated data.
        """
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Note` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('content', instance.content)
        instance.is_read_only = validated_data.get(
            'is_read_only', instance.is_read_only
        )
        validated_data.get(
            'is_expanded', instance.is_expanded
        )
        instance.syntax = validated_data.get('syntax', instance.syntax)
        instance.level = validated_data.get('level', instance.level)
        instance.ts_updated = timezone.now()
        instance.parent = validated_data.get('parent_note', instance.parent)

        instance.save()

        return instance
