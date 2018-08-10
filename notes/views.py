from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework import permissions

from notes.models import Note, Tag
from notes.serializers import NoteSerializer, TagModelSerializer
from notes.permissions import *


class NoteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

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
    permission_classes = [IsAdminOrIsSelf,]

    def get(self, request, user_id=None):
        notes = Note.objects.filter(owner__id=user_id)
        serializer = NoteSerializer(notes, many=True, context={'request': request})

        return Response(serializer.data)