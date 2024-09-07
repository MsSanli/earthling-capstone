from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from earthling_api.models import Subject, Language
from earthling_api.views.subject_view import SubjectSerializer

class SubjectTests(APITestCase):
    def setUp(self):
        self.language = Language.objects.create(
            name="Test Language",
            region="Test Region",
            number_of_speakers=1000000,
            pronunciation="Test Pronunciation",
            language_family="Test Family",
            writing_system="Test Writing System"
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            age=25,
            language=self.language,
            additional_info="Test info"
        )

    def test_create_subject(self):
        url = reverse('subject-list')
        subject_data = {
            "name": "New Subject",
            "age": 30,
            "language": self.language.id,
            "additional_info": "New info"
        }
        response = self.client.post(url, subject_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_subject = Subject.objects.last()
        expected = SubjectSerializer(new_subject)
        self.assertEqual(expected.data, response.data)

    def test_get_subject(self):
        url = reverse('subject-detail', args=[self.subject.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = SubjectSerializer(self.subject)
        self.assertEqual(expected.data, response.data)

    def test_list_subjects(self):
        url = reverse('subject-list')
        response = self.client.get(url)
        all_subjects = Subject.objects.all()
        expected = SubjectSerializer(all_subjects, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_update_subject(self):
        url = reverse('subject-detail', args=[self.subject.id])
        updated_subject = {
            "name": "Updated Subject",
            "age": 35,
        }
        response = self.client.patch(url, updated_subject, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.subject.refresh_from_db()
        self.assertEqual(updated_subject['name'], self.subject.name)
        self.assertEqual(updated_subject['age'], self.subject.age)

    def test_delete_subject(self):
        url = reverse('subject-detail', args=[self.subject.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_subject(self):
        url = reverse('subject-detail', args=[self.subject.id])
        updated_subject = {
            "name": "Updated Subject",
            "age": 35,
        }
        response = self.client.put(url, updated_subject, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.subject.refresh_from_db()
        self.assertEqual(updated_subject['name'], self.subject.name)
        self.assertEqual(updated_subject['age'], self.subject.age)
        
    def test_partial_update_subject(self):
        url = reverse('subject-detail', args=[self.subject.id])
        updated_data = {
            "name": "Partially Updated Subject",
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.subject.refresh_from_db()
        self.assertEqual(updated_data['name'], self.subject.name)
