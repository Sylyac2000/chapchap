""" Models of store application"""

from django.db import models
from frontend.models import Utilisateur
import uuid

from utils.utility import PathAndRename


class Store(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to=PathAndRename('uploads/store'), max_length=1000)
    code = models.CharField(default=uuid.uuid4, unique=True, max_length=100)
    phone = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    proprietary = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    datecreation = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    categoryimage = models.ImageField(upload_to='uploads/category')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    productimage = models.ImageField(upload_to='uploads/products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    datecreation = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
