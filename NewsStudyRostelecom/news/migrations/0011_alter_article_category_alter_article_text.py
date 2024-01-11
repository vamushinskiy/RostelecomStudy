# Generated by Django 4.2.7 on 2024-01-10 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_viewcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('ФП', 'Фактическая погода'), ('ПП', 'Прогноз погоды'), ('ШО', 'Штормовое оповещение'), ('ШП', 'Штормовое предупреждение'), ('КП', 'Карты погоды')], max_length=25, verbose_name='Категория сообщения'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(20, 'the field must contain at least 20 characters')], verbose_name='Текст сообщения'),
        ),
    ]