from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from earthling_api.models import Language
from earthling_api.views.language_view import LanguageSerializer

class LanguageTests(APITestCase):
    def setUp(self):
        self.language = Language.objects.create(
            name="Test Language",
            region="Test Region",
            number_of_speakers=1000000,
            pronunciation="Test Pronunciation",
            language_family="Test Family",
            writing_system="Test Writing System"
        )

    def test_create_language(self):
        url = reverse('language-list')
        language_data = {
            "name": "New Language",
            "region": "New Region",
            "number_of_speakers": 2000000,
            "pronunciation": "New Pronunciation",
            "language_family": "New Family",
            "writing_system": "New Writing System"
        }
        response = self.client.post(url, language_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_language = Language.objects.last()
        expected = LanguageSerializer(new_language)
        self.assertEqual(expected.data, response.data)

    def test_get_language(self):
        url = reverse('language-detail', args=[self.language.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = LanguageSerializer(self.language)
        self.assertEqual(expected.data, response.data)

    def test_list_languages(self):
        url = reverse('language-list')
        response = self.client.get(url)
        all_languages = Language.objects.all()
        expected = LanguageSerializer(all_languages, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_update_language(self):
        url = reverse('language-detail', args=[self.language.id])
        updated_language = {
            "name": "Updated Language",
            "number_of_speakers": 3000000,
        }
        response = self.client.put(url, updated_language, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.language.refresh_from_db()
        self.assertEqual(updated_language['name'], self.language.name)
        self.assertEqual(updated_language['number_of_speakers'], self.language.number_of_speakers)

    def test_partial_update_language(self):
        url = reverse('language-detail', args=[self.language.id])
        updated_data = {
            "name": "Partially Updated Language",
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.language.refresh_from_db()
        self.assertEqual(updated_data['name'], self.language.name)

    def test_delete_language(self):
        url = reverse('language-detail', args=[self.language.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
