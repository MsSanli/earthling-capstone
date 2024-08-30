from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from earthling_api.models import Entry, Tag, Subject, User

class EntrySerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True, read_only=True)

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
            'tag'
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

    def create(self, request):
        try:
            # Extract data from request
            user = User.objects.get(pk=request.data['user'])
            subject = Subject.objects.get(pk=request.data['subject'])
            
            # Create new entry
            entry = Entry.objects.create(
                user=user,
                subject=subject,
                date=request.data['date'],
                ipa_text=request.data['ipa_text'],
                meaning=request.data['meaning'],
                notes=request.data.get('notes', '')
            )

            # Handle tag
            tag = request.data.get('tag', [])
            for tag_name in tag:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                entry.tag.add(tag)

            serializer = EntrySerializer(entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except KeyError as e:
            return Response({'error': f'Missing required field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, Subject.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            entry = get_object_or_404(Entry, pk=pk)
            
            # Update fields
            entry.user = User.objects.get(pk=request.data.get('user', entry.user.id))
            entry.subject = Subject.objects.get(pk=request.data.get('subject', entry.subject.id))
            entry.date = request.data.get('date', entry.date)
            entry.ipa_text = request.data.get('ipa_text', entry.ipa_text)
            entry.meaning = request.data.get('meaning', entry.meaning)
            entry.notes = request.data.get('notes', entry.notes)
            entry.save()

            # Handle tag
            if 'tag' in request.data:
                new_tag = request.data['tag']
                # Clear existing tag
                entry.tag.clear()
                # Add new tag
                for tag_name in new_tag:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    entry.tag.add(tag)

            serializer = EntrySerializer(entry)
            return Response(serializer.data)
        
        except (User.DoesNotExist, Subject.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        entry = get_object_or_404(Entry, pk=pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
