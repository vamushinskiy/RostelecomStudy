# Generated by Django 4.2.7 on 2024-01-05 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_account_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
