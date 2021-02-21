from os import name
from django.db import models
from datetime import datetime

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=200, unique=True)
    price = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['publish_date']


class Child(models.Model):
    product = models.ForeignKey(
        Product, related_name='childs', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    details = models.TextField(max_length=1000, blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',  blank=False)
    photo2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.code
    
    class Meta:
        ordering = ['-publish_date']

  
