from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from earthling_api.models import User

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "uid": "testuid123"
        }
        self.user = User.objects.create(**self.user_data)

    def test_create_user(self):
        url = reverse('user-list')
        new_user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "uid": "newuseruid123"
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(email="newuser@example.com").name, "New User")

    def test_retrieve_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.user_data['name'])

    def test_update_user(self):
        url = reverse('user-detail', args=[self.user.id])
        updated_data = {
            "name": "Updated User",
            "email": "updated@example.com",
            "uid": "updateduid123"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Updated User")

    def test_delete_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

def test_retrieve_nonexistent_user(self):
    url = reverse('user-detail', args=[999])
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_with_invalid_data(self):
        url = reverse('user-list')
        invalid_user_data = {
            "name": "Invalid User",
            "email": "not_an_email",
            "uid": "invaliduid"
        }
        response = self.client.post(url, invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_partial_update_user(self):
    url = reverse('user-detail', args=[self.user.id])
    partial_data = {
        "name": "Partially Updated User"
    }
    response = self.client.patch(url, partial_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.user.refresh_from_db()
    self.assertEqual(self.user.name, "Partially Updated User")
    self.assertEqual(self.user.email, self.user_data['email'])  # Email should remain unchanged
