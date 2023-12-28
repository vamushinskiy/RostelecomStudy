from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('all_news', views.index, name='news_index'),
    path('show/<int:id>', views.detail, name='news_detail'),
    path('new_article', views.new_article, name='new_article')
]
