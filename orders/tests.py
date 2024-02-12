import json

from autoparts.models import Cart, Order, Product
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class OrderViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user321",
                                            password="stronguser321")

        Product(id=1, name="test_product_name", details="test product details").save()
        Product(id=2, name="test_product_2_name", details="test product 2 details").save()
        Cart(user_id=self.user.id, product_id=1, product_name="test_product_name", quantity=4).save()
        Cart(user_id=self.user.id, product_id=2, product_name="test_product_2_name", quantity=5).save()
        Order(user_id=self.user.id, order_id=2, products="1,2,6", date_time="2024-02-11T16:56:00Z").save()

        try:
            self.token = Token.objects.get(user_id=self.user.id)
        except Token.DoesNotExist:
            self.token = Token.objects.create(user=self.user)
        
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_order_items_authenticated(self):
        response = self.client.put(reverse("order-handler", kwargs={"pk": 1}), json.dumps({"date_time": "2024-02-14 11:26:00"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'date_time': '2024-02-14T11:26:00Z','order_id': 1,'products': '1,2','user_id': self.user.id})

    def test_order_items_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.put(reverse("order-handler", kwargs={"pk": 1}), json.dumps({"date_time": "2024-02-13 11:26:00"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content), {"detail": "Authentication credentials were not provided."})

    def test_order_view_authenticated(self):
        response = self.client.get(reverse("order-handler", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'delivery_date_time': '2024-02-11T16:56:00Z','items': ['test_product_name', 'test_product_2_name']})

    def test_order_view_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("order-handler", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content), {"detail": "Authentication credentials were not provided."})
