from django.contrib import admin
from . models import *
from django.db.models.functions import Length
from django.db.models import Count


# Создаём класс для загрузки нескольких изображений в одно сообщение
class ArticleImageInline(admin.TabularInline):
    model = Image
    extra = 3
    readonly_fields = ('id', 'image_tag')

class ArticleAdmin(admin.ModelAdmin):
    # Сортировка по полям
    ordering = ['-date', 'title']
    # отображаемые поля
    list_display = ['title', 'author', 'date', 'category', 'image_tag']
    # поля по которым возможна фильтрация
    list_filter = ['title', 'author', 'date', 'category']
    # поля сортировки по умолчанию
    list_display_links = ['date']
    # редактируемые поля
    #list_editable = ['title']
    # нередактируемые поля
    #readonly_fields = ['category']
    # Для автоматического формирования слаг
    prepopulated_fields = {"slug" : ('title',)}
    # Пагинация
    list_per_page = 5
    # Добавление картинок в сообщение
    inlines = [ArticleImageInline,]
    # Добавление поиска
    search_fields = ['title__icontains','tags__title']


    @admin.display(description='Длина сообщения')
    def symbols_count(self, article:Article):
        return f"Кол-во символов: {len(article.text)}"

# Регистрация в панели администрирования через декоратор.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'tag_count']
    list_filter = ['title', 'status']
# При регистрация в панели администрирования через декоратор следущая строчка не нужна..
#admin.site.register(Tag, TagAdmin)

    @admin.display(description='Повторений', ordering='tag_count')
    def tag_count(self, object):
        return object.tag_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset
admin.site.register(Article, ArticleAdmin)

# для отображения картинок в сообщениях.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','article','image_tag']