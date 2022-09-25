import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
                "username": "testCase",
                "password": "newTestCase",
                "password2": "newTestCase",
                "email": "newTestCase@gmail.com",
                "first_name": "test",
                "last_name": "case"
                }
        response = self.client.post("/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
