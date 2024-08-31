# from django.http import HttpResponseServerError
# from django.shortcuts import get_object_or_404
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers, status
# from earthling_api.models import EntryTag

# class EntryTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EntryTag
#         fields = ['id', 'entry', 'tag']

# # ViewSet for EntryTag model
# class EntryTagViewSet(ViewSet):

#     # def create(self, request):
#     #     serializer = EntryTagSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         entry_tag = get_object_or_404(EntryTag, pk=pk)
#         serializer = EntryTagSerializer(entry_tag)
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         entry_tag = get_object_or_404(EntryTag, pk=pk)
#         entry_tag.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
