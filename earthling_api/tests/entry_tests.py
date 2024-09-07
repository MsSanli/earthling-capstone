from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from earthling_api.models import Entry, User, Subject, Tag, Language
from datetime import datetime

class EntryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="Test User", email="test@example.com", uid="testuid123")
        
        # Create a test language with number_of_speakers
        self.language = Language.objects.create(
            name="Test Language",
            number_of_speakers=1000000  # Add an appropriate number here
        )
        
        # Create a subject with all required fields
        self.subject = Subject.objects.create(
            name="Test Subject",
            age=25,
            language=self.language
        )
        
        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")
        
        self.entry_data = {
            "user": self.user.id,
            "subject": self.subject.id,
            "date": "2023-06-15T10:00:00Z",
            "ipa_text": "test_ipa",
            "meaning": "test meaning",
            "notes": "test notes",
            "tag": ["Tag1", "Tag2"]
        }
        
        self.entry = Entry.objects.create(
            user=self.user,
            subject=self.subject,
            date="2023-06-15T10:00:00Z",
            ipa_text="existing_ipa",
            meaning="existing meaning",
            notes="existing notes"
        )
        self.entry.tag.add(self.tag1)

    def test_create_entry(self):
        url = reverse('entry-list')
        response = self.client.post(url, self.entry_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 2)
        self.assertEqual(Entry.objects.get(ipa_text="test_ipa").meaning, "test meaning")

    def test_retrieve_entry(self):
        url = reverse('entry-detail', args=[self.entry.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ipa_text'], "existing_ipa")

    def test_update_entry(self):
        url = reverse('entry-detail', args=[self.entry.id])
        new_language = Language.objects.create(name="New Test Language", number_of_speakers=2000000)
        new_subject = Subject.objects.create(name="New Test Subject", age=30, language=new_language)
        updated_data = {
            "ipa_text": "updated_ipa",
            "meaning": "updated meaning",
            "subject": new_subject.id,
            "tag": ["Tag2", "NewTag"]
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.ipa_text, "updated_ipa")
        self.assertEqual(self.entry.meaning, "updated meaning")
        self.assertEqual(self.entry.subject, new_subject)
        self.assertEqual(self.entry.tag.count(), 2)
        self.assertTrue(self.entry.tag.filter(name="NewTag").exists())

    def test_delete_entry(self):
        url = reverse('entry-detail', args=[self.entry.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Entry.objects.count(), 0)

    def test_list_entries(self):
        url = reverse('entry-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_entry_with_invalid_data(self):
        url = reverse('entry-list')
        invalid_data = self.entry_data.copy()
        invalid_data.pop('user')  # Remove required field
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_entry_with_nonexistent_user(self):
        url = reverse('entry-detail', args=[self.entry.id])
        invalid_data = {"user": 9999}  # Non-existent user ID
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_entry(self):
        url = reverse('entry-detail', args=[9999])  # Non-existent entry ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
