# Generated by Django 4.2.7 on 2024-01-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_account_address_account_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='telegram',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
