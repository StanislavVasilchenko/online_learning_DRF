from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email address')
    phone = models.CharField(max_length=20, verbose_name='phone number', blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name='city', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='avatar', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
