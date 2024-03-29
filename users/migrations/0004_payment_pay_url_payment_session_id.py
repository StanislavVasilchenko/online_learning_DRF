# Generated by Django 4.2.7 on 2024-02-25 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='pay_url',
            field=models.URLField(blank=True, null=True, verbose_name='ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='payment',
            name='session_id',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='id_сессии'),
        ),
    ]
