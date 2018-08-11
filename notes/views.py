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

from notes.models import Note, Tag
from notes.serializers import NoteSerializer, TagModelSerializer
from notes.permissions import *


class NoteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = [IsAdminOrIsSelf]
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def create(self, request):
        user = request.user
        data = request.data

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
            exists_query &= Q(parent=data['parent'])

        if Note.objects.filter(exists_query).exists():
            resp = {
                'detail': 'Note with the same name is already exists.'
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        # Create the note
        note = Note.objects.create(**data)
        serializer = NoteSerializer(note, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        notes = Note.objects.filter(owner=request.user)\
            .select_related('owner', 'parent')
        serializer = NoteSerializer(notes, many=True, context={'request': request})

        return Response(serializer.data)

    @action(
        methods=['get', 'post'], detail=True,
        permission_classes=[IsAdminOrIsSelf], url_name='children'
    )
    def children(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        children = note.children.all()
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
        serializer = NoteSerializer(notes, many=True, context={'request': request})

        return Response(serializer.data)