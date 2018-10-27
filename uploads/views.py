from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from notes.models import File
from notes.serializers import FileModelSerializer

from datetime import datetime

class UploadsListAPIView(views.APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        files = File.objects.filter(owner=request.user)
        serializer = FileModelSerializer(
            files, many=True, context={'request': request}
        )

        return Response(serializer.data)


    def put(self, request, file_name=None):
        file_data = request.data
        print(file_data)

        if file_name is None:
            file_name = "file_{}".format(datetime.now())

        return Response(status=204)