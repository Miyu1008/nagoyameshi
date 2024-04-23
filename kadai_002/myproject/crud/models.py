from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission  # GroupとPermissionをインポート
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from accounts.models import CustomUser as User

class User(AbstractUser):
    email = models.EmailField('メールアドレス', unique=True)
    is_store = models.BooleanField(default=False)

    # groupsフィールドとuser_permissionsフィールドをUserクラス内に移動し、'to'引数を追加
    groups = models.ManyToManyField(
        Group,  # 'to'引数にGroupモデルを指定
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="crud_user_groups",  # related_nameを追加
        related_query_name="user",
        # through='UserGroups'  # 中間モデルの指定が必要な場合にはコメントを解除してください
    )
    user_permissions = models.ManyToManyField(
        Permission,  # 'to'引数にPermissionモデルを指定
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="crud_user_permissions",  # related_nameを追加
        related_query_name="user",
        # through='UserUserPermissions'  # 中間モデルの指定が必要な場合にはコメントを解除してください
    )

    
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

