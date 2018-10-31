from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
)
from rest_framework import permissions

from notes.models import Note, Tag, User
from notes.serializers import (
    NoteSerializer,
    TagModelSerializer,
    PartialNoteSerializer,
    SimplifiedNoteSerializer,
)
from notes.permissions import *


class NoteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrIsSelf]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def update(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        data = dict(request.data)

        # When note's parent will be updated, we need to remove
        # this note from previous parent children list and add
        # it to new parent children list
        parent_upd = data.get('parent', {}) or {}
        parent_upd_id = parent_upd.get('id', None)
        if parent_upd_id is not None and note.parent.id != parent_upd_id:
            parent_upd = get_object_or_404(Note, id=parent_upd_id)
            data['parent_note'] = parent_upd

            note.parent.children.remove(note)
            parent_upd.children.add(note)
            # Updating current note level
            data['level'] = parent_upd.level + 1

        serializer = NoteSerializer(
            note, data,
            context={'request': request}, 
            partial=True
        )
        serializer.is_valid()
        serializer.update(note, data)
        
        return Response(serializer.data)

    # TODO: saving data with NoteSerializer
    def create(self, request):
        user = request.user
        data = dict(request.data)

        data['owner'] = user
        user_filter = Q(owner=user)

        # Note's name may not be empty string
        if not data.get('name'):
            resp = {
                'detail': 'Name field may not be empty.'
            }
            return Response(resp, status=status.HTTP_409_CONFLICT)

        # Setting up default values
        if data.get('level') is None:
            data['level'] = 0
        if data.get('syntax') is None:
            data['syntax'] = 'SI'
        if data.get('tags') is None:
            data['tags'] = []

        parent_note = None
        if data.get('parent'):
            # Increase nesting level of the note will be created
            parent_note = Note.objects.get(id=int(data.get('parent')))
            data['level'] = parent_note.level + 1
            # Converting string note ID to `Note` instance
            data['parent'] = parent_note


        # Check if note with this name exists
        exists_query = user_filter & Q(name=data['name'])
        if parent_note:
            exists_query &= Q(parent=parent_note)

        if Note.objects.filter(exists_query).exists():
            resp = {
                'detail': 'Note with the same name is already exists.'
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        # Create the note
        note = Note.objects.create(**data)
        serializer = NoteSerializer(note, context={'request': request})

        # If parent is set update it's children list too
        if parent_note:
            parent_note.children.add(note)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        # `show_all` argument for disabling filtering by user
        # Option is available for admin only
        show_all = request.query_params.get('show_all', 0)
        if not request.user.is_superuser:
            show_all = 0

        query_filter = Q()
        # Select 0 level only hierarchy nodes
        #query_filter &= Q(level=0)

        user_filter = Q(owner=request.user)
        if not show_all:
            query_filter &= user_filter

        notes = Note.objects.filter(query_filter)\
            .select_related('owner', 'parent')
        serializer = SimplifiedNoteSerializer( #NoteSerializer(
            notes, many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    @action(
        methods=['get', 'post'], detail=True,
        permission_classes=[IsAdminOrIsSelf], url_name='children'
    )
    def children(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        children = note.children.filter(parent__id=note.id)
        serializer = NoteSerializer(
            children, many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    @action(
        methods=['get', 'post'], detail=True,
        permission_classes=[IsAdminOrIsSelf], url_name='tags'
    )
    def tags(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        tags = note.tags.all().first()
        serializer = TagModelSerializer(tags, context={'request': request})

        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer

class UserNotesAPIView(APIView):
    """
    List only specific user notes.
    """
    permission_classes = [IsAdminOrIsSelf]
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, user_id=None):
        notes = Note.objects.filter(owner__id=user_id)
        serializer = NoteSerializer(
            notes, many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request, user_id=None):
        owner = get_object_or_404(User, id=user_id)
        handle_uploaded_file(request.FILES['file'], owner)


def handle_uploaded_file(f, owner):
    import sqlite3
    conn = sqlite3.connect(f)
    cur = conn.cursor()

    notes_map = dict()
    for pk, title, txt, syntax, tags, is_ro,\
        is_rich_text, has_codebox, has_table,\
        has_image, level in cur.execute("SELECT * FROM node"):

        txt = parse_txt(txt)
        syntax = "CU" if 'cu' in syntax else "SI"
        note = Note.objects.create(name=title, content=txt, syntax=syntax, tags=tags, is_read_only=bool(is_ro),
                                      is_expanded=is_rich_text, has_code_box=has_codebox, has_table=has_table,
                                      has_image=has_image, level=level, owner=owner)
        notes_map[pk] = note.pk

    for pk, parent, seq \
            in cur.execute("SELECT * FROM children"):
            note = Note.objects.get(pk=notes_map[pk])
            parent_node_id = notes_map.get(parent)
            if parent_node_id:
                parent = Note.objects.get(pk=notes_map[parent])
                note.parent = parent
                note.save()
                parent.children.add(note)

#TODO:
def parse_txt(txt):
    """Parse cherry tree XML into HTML"""
    return txt
