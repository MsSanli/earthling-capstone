from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from earthling_api.models import Entry, Tag

class EntrySerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Entry
        fields = [
            'id', 
            'user', 
            'subject', 
            'date', 
            'ipa_text', 
            'meaning', 
            'notes', 
            'created_at',
            'tags'
        ]

class EntryView(ViewSet):
    def retrieve(self, request, pk=None):
        entry = get_object_or_404(Entry, pk=pk)
        serializer = EntrySerializer(entry)
        return Response(serializer.data)

    def list(self, request):
        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)
      
    def destroy(self, request, pk):
        entry = get_object_or_404(Entry, pk=pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def add_tag(self, request, pk=None):
        entry = get_object_or_404(Entry, pk=pk)
        tag_name = request.data.get('tag')
        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            entry.tags.add(tag)
            return Response({'status': 'tag added'})
        return Response({'error': 'tag name is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_tag(self, request, pk=None):
        entry = get_object_or_404(Entry, pk=pk)
        tag_name = request.data.get('tag')
        if tag_name:
            tag = Tag.objects.filter(name=tag_name).first()
            if tag:
                entry.tags.remove(tag)
                return Response({'status': 'tag removed'})
            return Response({'error': 'tag not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'tag name is required'}, status=status.HTTP_400_BAD_REQUEST)
