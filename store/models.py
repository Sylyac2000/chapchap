#!/usr/bin/env python
""" Models of store application"""


from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from frontend.models import Utilisateur
import uuid

from utils.utility import PathAndRename


class Store(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to=PathAndRename('uploads/store'), max_length=1000)
    code = models.CharField(default=uuid.uuid4, unique=True, max_length=100)
    phone = models.CharField(max_length=20)
    description = models.TextField()
    proprietary = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    datecreation = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)
    qrcode = models.ImageField(upload_to=PathAndRename('uploads/store/qrcode'), default='uploads/store/noimage.png')

    photo_thumbnail = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(350, 200)],
                                     format='JPEG',
                                     options={'quality': 60})  # < here

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('frontend:detail-store', args=[self.code])


class Category(models.Model):
    name = models.CharField(max_length=50)
    categoryimage = models.ImageField(upload_to='uploads/category')

    categoryimage_thumbnail = ImageSpecField(source='categoryimage',
                                     processors=[ResizeToFill(350, 200)],
                                     format='JPEG',
                                     options={'quality': 60})  # < here

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['name'])
        ]


class Product(models.Model):
    """product model"""
    name = models.CharField(max_length=50)
    description = models.TextField()
    productimage = models.ImageField(upload_to='uploads/products/%Y/%m/%d')
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    datecreation = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)


    productimage_thumbnail = ImageSpecField(source='productimage',
                                     processors=[ResizeToFill(350, 200)],
                                     format='JPEG',
                                     options={'quality': 60})  # < here

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-datecreation']),
        ]


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:edit-product', args=[self.id])
