from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from earthling_api.models import Language

class LanguageView(ViewSet):  # type: ignore
  def retrieve(self, request, pk):
      language = get_object_or_404(Language, pk=pk)
      serializer = LanguageSerializer(language)
      return Response(serializer.data)
    
#all languages
  def list(self, request):
      languages = Language.objects.all()
      serializer = LanguageSerializer(languages, many=True)
      return Response(serializer.data)

  def destroy(self, request, pk):
      language = get_object_or_404(Language, pk=pk)
      language.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'region', 'number_of_speakers', 'pronunciation', 'language_family', 'writing_system']
