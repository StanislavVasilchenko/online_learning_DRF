from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import AUTH_USER_MODEL
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email address')
    phone = models.CharField(max_length=20, verbose_name='phone number', blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name='city', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='avatar', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payment(models.Model):
    CASH = 'наличные'
    CARD = 'карта'
    PAYMENT_METHOD = ((CASH, 'наличные'),
                      (CARD, 'карта')
                      )

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_payments', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_payments', blank=True, null=True)
    date = models.DateTimeField(verbose_name='дата оплаты', auto_now_add=True)
    amount = models.DecimalField(verbose_name='сумма оплаты', blank=True, null=True, max_digits=10, decimal_places=2)
    method = models.CharField(verbose_name='способ оплаты', max_length=25, choices=PAYMENT_METHOD, default=CARD)

    pay_url = models.URLField(max_length=500, verbose_name='ссылка на оплату', blank=True, null=True)
    session_id = models.CharField(max_length=500, verbose_name='id_сессии', blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.method}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
