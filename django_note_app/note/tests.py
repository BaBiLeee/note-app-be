from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django import setup
import os
os.environ.setdefault("DJANGO_SETTING_MODULE", "django_note_app.settings")
setup()


class UserTestCase(TestCase):
# Create your tests here.
    def test_user_list_get_request(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('data', response.data)
        self.assertEqual(response.data['message'], 'Successfully retrieved user data')
        self.assertIsInstance(response.data['data'], list)