from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from earthling_api.models import Entry

class EntryView(ViewSet):
  
#single entry
    def retrieve(self, request, pk=None):
        entry = get_object_or_404(Entry, pk=pk)
        serializer = EntrySerializer(entry)
        return Response(serializer.data)

#all entries
    def list(self, request):
        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)


class EntrySerializer(serializers.ModelSerializer):
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
            'created_at'
        ]
