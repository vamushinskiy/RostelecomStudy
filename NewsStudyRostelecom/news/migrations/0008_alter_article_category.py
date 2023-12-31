# Generated by Django 4.2.7 on 2023-12-30 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('ФП', 'Фактическая погода'), ('ПП', 'Прогноз погоды'), ('ШО', 'Штормовое оповещение'), ('ШП', 'Штормовое предупреждение'), ('КП', 'Карты погоды')], max_length=20, verbose_name='Категория сообщения'),
        ),
    ]
