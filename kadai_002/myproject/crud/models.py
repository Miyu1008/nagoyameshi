from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission  # GroupとPermissionをインポート
from django.utils import timezone
from datetime import datetime
from django.conf import settings

    
class Store(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=200, default='Tokyo, Japan', blank=True) 
    phone_number = models.CharField(max_length=20, default='')
    image = models.ImageField(upload_to='images/', default='images/default_image.png')
    
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    email = models.EmailField()

class Table(models.Model):
    seats = models.IntegerField()
    min_people = models.IntegerField()
    max_people = models.IntegerField()

