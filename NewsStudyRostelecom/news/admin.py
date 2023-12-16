from django.contrib import admin
from . models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date', 'category']
    list_filter = ['title', 'author', 'date', 'category']

admin.site.register(Article, ArticleAdmin)