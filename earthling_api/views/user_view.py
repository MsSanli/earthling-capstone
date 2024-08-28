from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from earthling_api.models import User

class UserView(ViewSet):

    def retrieve(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serialized = UserSerializer(user, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        user = User.objects.all()
        serialized = UserSerializer(user, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        """
        function to delete a user
        """
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "name", "email", "created_at", "last_login", "uid")
