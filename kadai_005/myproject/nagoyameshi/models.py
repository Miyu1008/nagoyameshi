from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import date


#ユーザー
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        # ここでemailを必須とします
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        user_type = models.CharField(max_length=30, default='default_value')


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
      (1, 'user'),
      (2, 'store'),
    )

    email = models.EmailField(unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    
    email = models.EmailField('メールアドレス', unique=True)
    first_name = models.CharField(('姓'), max_length=30)
    last_name = models.CharField(('名'), max_length=30)
    description = models.TextField('自己紹介', default="", blank=True)
    image = models.ImageField(upload_to='images', verbose_name='プロフィール画像', null=True, blank=True)

    # Django管理サイトで権限をハンドルするためのもの
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



#店舗
class Store(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=200, default='Tokyo, Japan', blank=True) 
    phone_number = models.CharField(max_length=20, default='')
    image = models.ImageField(upload_to='static/images/', default='static/images/default_image.png')
    available_dates = models.ManyToManyField('Date', blank=True)

    def __str__(self):
        return self.name    

class Date(models.Model):
    date = models.DateField()



#店舗予約
class Schedule(models.Model):
    """予約スケジュール."""
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    name = models.CharField('予約者名', max_length=255)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.name} {start} ~ {end} {self.staff}'
    




class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name
     
    def get_absolute_url(self):
        return reverse('list')
    



class Booking(models.Model):
    #staff = models.ForeignKey(Staff, verbose_name='スタッフ', on_delete=models.CASCADE)
    first_name = models.CharField('姓', max_length=100, null=True, blank=True)
    last_name = models.CharField('名', max_length=100, null=True, blank=True)
    tel = models.CharField('電話番号', max_length=100, null=True, blank=True)
    remarks = models.TextField('備考', default="", blank=True)
    start = models.DateTimeField('開始時間', default=timezone.now)
    end = models.DateTimeField('終了時間', default=timezone.now)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M')
        return f'{self.first_name}{self.last_name} {start} ~ {end} {self.staff}'

#お気に入り
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)  # Store モデルに適切な名前で修正する
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'store')  # ユーザーごとに同じ店舗を複数回お気に入りに登録できないように設定