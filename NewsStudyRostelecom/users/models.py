from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    post_choices = (('НМтС', 'Начальник метеослужбы'),
                    ('НС', 'Начальник смены'),
                    ('ИС', 'Инженер-синоптик'),
                    ('МН', 'Метеонаблюдатель'),
                    ('N/A', 'Not answered'))
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    nickname = models.CharField(max_length=100)
    birthdate = models.DateField(null=True)
    post = models.CharField(choices=post_choices, max_length=20)
    point = models.CharField(max_length=25, default='0')
    account_image = models.ImageField(default='default.jpg',
                                      upload_to='account_images')

    # pip install pillow в терминале для работы с изображениями.

    def __str__(self):
        return f"{self.user.username}'s account"