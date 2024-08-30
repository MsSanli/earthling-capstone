from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from earthling_api.models import Tag

class TagView(ViewSet):
    # single tag
    def retrieve(self, request, pk=None):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    # multiple tag, not sure if this is needed
    def list(self, request):
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)
  
    def destroy(self, request, pk=None):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
