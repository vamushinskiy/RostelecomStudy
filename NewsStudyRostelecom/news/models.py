from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Count



class Tag(models.Model):
    title = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title

    # def tag_count(self, object):
    #     count = self.objects.annotate(tag_count=Count('article')

    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Явление'
        verbose_name_plural ='Явления'

class Article(models.Model):
    categories = (('ФП', 'Фактическая погода'),
                  ('ПП', 'Прогноз погоды'),
                  ('ШО', 'Штормовое оповещение'),
                  ('ШП', 'Штормовое предупреждение'),
                  ('КП', 'Карты погоды'))

    # поля                                   # models.CASCADE или SET_DEFAULT
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    title = models.CharField('Пункт', max_length=50, default='')
    category = models.CharField(choices=categories, max_length=20, verbose_name='Категория сообщения')
    anouncement = models.TextField('Анонс', max_length=250)
    text = models.TextField('Текст сообщения')
    date = models.DateTimeField('Дата наблюдения', auto_created=True)
    tags = models.ManyToManyField(to=Tag, blank=True, verbose_name='Явления')
    slug = models.SlugField()

    # методы моделей
    def __str__(self):
        return f' {self.title} от: {str(self.date)[:16]}'

    def get_absolute_url(self):
        return f'/news/show/{self.id}'

    def image_tag(self):
        image = Image.objects.filter(article=self)
        if image:
            return mark_safe('<img src="{self.image.url}" height="50px" width="auto"/>')
            # return mark_safe(f'<img src="{image[0].image.url}" height="50px" width="auto"/>')
        else:
            return '(no image)'

# создаём список тэгов
#     def tag_list(self):
#         s = ''
#         for t in self.tags:
#             s += t.title + ' '
#         return s
    # метаданные модели
    class Meta:
        ordering = ['-date', 'title']
        verbose_name = 'Сообщение'
        verbose_name_plural ='Сообщения'

# Для отображения картинок в сообщениях.
class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='article_images/%Y/%m/%d/')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="{self.image.url}" height="50px" width="auto"/>')
        else:
            return '(no image)'