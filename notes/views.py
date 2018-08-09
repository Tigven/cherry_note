from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, viewsets

from notes.models import Note
from notes.serializers import NoteSerializer

from rest_framework.permissions import (
    AllowAny,
)

class NoteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NotesListAPIView(APIView):
    """
    List all notes, or create a new note.
    """
    permission_classes = (AllowAny, )

    def get(self, *args, **kwargs):
        notes = Note.objects.all().select_related('parent')
        serializer = NoteSerializer(notes, many=True)

        return Response(serializer.data)