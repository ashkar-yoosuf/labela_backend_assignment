from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.name # making the object access descriptive

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})


class Cart(models.Model):
    user_id = models.IntegerField(null=False)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField()


class Order(models.Model):
    user_id = models.IntegerField(null=False)
    order_id = models.IntegerField(null=False)
    products = models.TextField()
    date_time = models.DateTimeField(null=False)
