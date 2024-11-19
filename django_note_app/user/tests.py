# tests.py
from rest_framework.test import APITestCase
from django.urls import reverse
from user.models import User
from rest_framework.exceptions import ValidationError
from .serializers import SimpleUserSerializer
from rest_framework import status
class UserTest(APITestCase):

    def setUp(self):
        # Create some test users
        user1 = User.objects.create_user(fullname="user1", email="user1@example.com", password="password123")
        user2 = User.objects.create_user(fullname="user2", email="user2@example.com", password="password123")
        self.client.force_authenticate(user=user1)

    def test_register_user(self):
        self.authenticate_user(self.user1)
        response = self.client.get('userList/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)