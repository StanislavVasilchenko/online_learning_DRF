from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='курс')
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    preview = models.ImageField(upload_to='materials/preview', verbose_name='превью', blank=True, null=True)
    user = models.ForeignKey('users.User', verbose_name='пользователь', on_delete=models.CASCADE,
                             blank=True, null=True)
    price = models.PositiveIntegerField(default=10000, verbose_name='Ценв')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='урок')
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    preview = models.ImageField(upload_to='materials/lesson', verbose_name='превью', blank=True, null=True)
    video_url = models.URLField(verbose_name='ссылка на видео', blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.SET_NULL, related_name='lessons',
                               null=True)
    user = models.ForeignKey('users.User', verbose_name='пользователь', on_delete=models.CASCADE,
                             blank=True, null=True)
    price = models.PositiveIntegerField(default=10000, verbose_name='Ценв')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name', 'course', ]


class Subscription(models.Model):
    user = models.ForeignKey('users.User', verbose_name='Пользователь', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE, related_name='course')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
