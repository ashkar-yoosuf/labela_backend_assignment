import json

from autoparts.models import Cart, Product
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class CartViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user321",
                                            password="stronguser321")

        Product(id=1, name="test_product_name", details="test product details").save()
        Product(id=2, name="test_product_2_name", details="test product 2 details").save()
        Cart(user_id=self.user.id, product_id=1, product_name="test_product_name", quantity=4).save()

        try:
            self.token = Token.objects.get(user_id=self.user.id)
        except Token.DoesNotExist:
            self.token = Token.objects.create(user=self.user)
        
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_cart_add_authenticated(self):
        response = self.client.put("/cart/", json.dumps({ "product_id":1, "quantity": 5 }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'product_id': 1,'product_name': 'test_product_name', 'quantity': 5, 'user_id': self.user.id})

    def test_cart_add_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.put("/cart/", json.dumps({ "product_id":1, "quantity": 5 }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content), {"detail": "Authentication credentials were not provided."})

    def test_cart_view_authenticated(self):
        response = self.client.get("/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'description': [{'product_id':1, 'product_name': 'test_product_name', 'quantity': 4}]})

    def test_cart_view_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/cart/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content), {"detail": "Authentication credentials were not provided."})

    def test_cart_delete_authenticated(self):
        response = self.client.delete(reverse("cart-delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cart_delete_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse("cart-delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content), {"detail": "Authentication credentials were not provided."})
