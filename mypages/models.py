from os import name
from django.db import models
from datetime import datetime
from products.models import Product
# Create your models here.


class Myslider(models.Model):
    product = models.ForeignKey(
        Product, related_name='MysSliChild', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    link = models.CharField(max_length=200, blank=True)
    link_number = models.PositiveIntegerField(default='5')
    URL = models.URLField(max_length=5000)
    slider_number = models.PositiveIntegerField(default='5')
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name



class Mysection(models.Model):
    product = models.ForeignKey(
        Product, related_name='MyChild', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    secName = models.CharField(max_length=200, default="none")
    details = models.TextField(max_length=1000)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',  blank=False)
    
    def __str__(self):
        return self.name