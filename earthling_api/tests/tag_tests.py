from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from earthling_api.models import Tag
from earthling_api.views.tag_view import TagSerializer

class TagTests(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")

    def test_create_tag(self):
        url = reverse('tag-list')
        tag_data = {"name": "New Tag"}
        response = self.client.post(url, tag_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_tag = Tag.objects.get(name="New Tag")
        expected = TagSerializer(new_tag)
        self.assertEqual(expected.data, response.data)

    def test_get_tag(self):
        url = reverse('tag-detail', args=[self.tag.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = TagSerializer(self.tag)
        self.assertEqual(expected.data, response.data)

    def test_list_tags(self):
        url = reverse('tag-list')
        response = self.client.get(url)
        all_tags = Tag.objects.all()
        expected = TagSerializer(all_tags, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_update_tag(self):
        url = reverse('tag-detail', args=[self.tag.id])
        updated_tag = {"name": "Updated Tag"}
        response = self.client.put(url, updated_tag, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.tag.refresh_from_db()
        self.assertEqual(updated_tag['name'], self.tag.name)

    def test_delete_tag(self):
        url = reverse('tag-detail', args=[self.tag.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(id=self.tag.id)
