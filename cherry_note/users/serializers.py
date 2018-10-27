from cherry_note.users.models import User
from rest_framework import serializers, viewsets
from rest_framework.reverse import reverse
from rest_framework.response import Response

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff',)

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #def retrieve(self, request, *args, **kwargs):
    #    notes_url = reverse(
    #        viewname='user_notes',
    #        request=request,
    #    )
    #    serializer = UserSerializer(self.queryset, context={'request': request})
    #    data = serializer.data
    #    data['notes'] = notes_url
    #    return Response(data)