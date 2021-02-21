from os import name
from django.db import models
from datetime import datetime

# Create your models here.


class Slider(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    link_number = models.PositiveIntegerField(default='5')
    URL = models.URLField(max_length=5000)
    slider_number = models.PositiveIntegerField(default='5')
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Slider2(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Slider3(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
