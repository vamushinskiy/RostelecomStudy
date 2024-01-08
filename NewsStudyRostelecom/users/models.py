from django.db import models
from django.contrib.auth.models import User
from news.models import Article


class Account(models.Model):
    post_choices = (('N/A', 'Not answered'),
                    ('НМтС', 'Начальник метеослужбы'),
                    ('НС', 'Начальник смены'),
                    ('ИС', 'Инженер-синоптик'),
                    ('МН', 'Метеонаблюдатель'))

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    nickname = models.CharField(max_length=100)
    birthdate = models.DateField(null=True)
    post = models.CharField(choices=post_choices, max_length=20, null=True)
    point = models.CharField(max_length=25, null=True)
    account_image = models.ImageField(default='default.jpg',
                                      upload_to='account_images')
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    telegram = models.CharField(max_length=100, null=True)

    # pip install pillow в терминале для работы с изображениями.

    def __str__(self):
        return f"{self.user.username}'s account"

    class Meta:
        ordering = ['user', 'point']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class FavoriteArticle(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    article = models.ForeignKey(Article,on_delete=models.SET_NULL,null=True)
    create_at=models.DateTimeField(auto_now_add=True)