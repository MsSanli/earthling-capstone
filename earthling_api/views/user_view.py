from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from earthling_api.models import User

class UserView(ViewSet):

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serialized = UserSerializer(user, context={'request': request})
        return Response(serialized.data)

    def list(self, request):
        user = User.objects.all()
        serialized = UserSerializer(user, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        """
        function to delete a user
        """
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
    def create(self, request):
        """
        Function to create a new user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Function to update a user
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "name", "email", "created_at", "last_login", "uid")
