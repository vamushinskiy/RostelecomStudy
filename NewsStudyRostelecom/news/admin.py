from django.contrib import admin
from . models import *

class ArticleAdmin(admin.ModelAdmin):
    # Сортировка по полям
    ordering = ['-date', 'title']
    # отображаемые поля
    list_display = ['title', 'author', 'date', 'category', 'symbols_count']
    # поля по которым возможна фильтрация
    list_filter = ['title', 'author', 'date', 'category']
    # поля сортировки по умолчанию
    list_display_links = ['date']
    # редактируемые поля
    list_editable = ['title']
    # нередактируемые поля
    #readonly_fields = ['category']
    # Для автоматического формирования слаг
    prepopulated_fields = {"slug" : ('title', 'date')}
    # Пагинация
    list_per_page = 6

    @admin.display(description='Длина сообщения')
    def symbols_count(self, article:Article):
        return f"Кол-во символов: {len(article.text)}"

# Регистрация в панели администрирования через декоратор.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['title', 'status']
# При регистрация в панели администрирования через декоратор следущая строчка не нужна..
#admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)