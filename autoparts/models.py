from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.name # making the object access descriptive

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # delete cart in case of User deletetion
    cart_id = models.IntegerField(null=True)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField()

class Delivery(models.Model):
    cart_id = models.IntegerField()
    date = models.TextField()