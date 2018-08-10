from rest_framework import serializers
from rest_framework.reverse import reverse
from notes.models import Note, Tag

"""
class NoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'name', 'is_read_only',)
"""

class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('name',)

class NoteChildrenHyperlink(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        url = reverse(
            viewname='note-children', args=[obj.pk.instance.id],
            request=request, format=format
        )
        return url

class NoteTagsHyperlink(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        url = reverse(
            viewname='note-tags', args=[obj.pk.instance.id],
            request=request, format=format
        )
        return url

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
    has_code_box = serializers.BooleanField(required=False, read_only=True)
    has_table = serializers.BooleanField(required=False, read_only=True)
    has_image = serializers.BooleanField(required=False, read_only=True)
    has_file = serializers.BooleanField(required=False, read_only=True)
    level = serializers.IntegerField(required=False)
    ts_created = serializers.DateTimeField(read_only=True)
    ts_updated = serializers.DateTimeField(read_only=True)
    is_read_only = serializers.BooleanField(required=False)

    owner = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
    )
    parent = serializers.HyperlinkedRelatedField(
        view_name='note-detail',
        queryset=Note.objects.all()[:30],
    )
    #tags = NoteTagsHyperlink(
    #    view_name='note-tags',
    #    read_only=True,
    #)
    tags = TagModelSerializer(
        many=True, #read_only=True,
        #queryset=Tag.objects.all(),
    )
    children = NoteChildrenHyperlink(
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
        instance.syntax = validated_data.get('syntax', instance.syntax)
        instance.style = validated_data.get('style', instance.style)
        instance.level = validated_data.get('level', instance.level)

        instance.save()

        return instance
