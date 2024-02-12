import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from autoparts.models import Product


class ProductViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user321",
                                            password="stronguser321")
        
        Product(id=1, name="test_product_name", details="test product details").save()

        try:
            self.token = Token.objects.get(user_id=self.user.id)
        except Token.DoesNotExist:
            self.token = Token.objects.create(user=self.user)
        
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_list_product_authenticated(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_product_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_detail_authenticated(self):
        response = self.client.get(reverse("product-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_product_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("product-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
