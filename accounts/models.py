from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Child

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_favorites = models.ManyToManyField(Child, blank=True)
    address = models.CharField(max_length=100)
    tell = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
