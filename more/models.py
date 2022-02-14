from os import name
from django.db import models
from datetime import datetime
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.urls import reverse

# Create your models here.

class Work(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField(max_length=2000, blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',  blank=False)
    photo2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    photo4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    photo5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    photo6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    photo7 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    photo8 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    video = models.FileField(upload_to='videos_uploaded',blank=True, null=True)
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-publish_date']