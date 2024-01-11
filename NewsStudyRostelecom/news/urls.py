from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('all_news', views.index, name='news_index'),
    path('show/<int:pk>', views.ArticleDetailView.as_view(), name='news_detail'),
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='delete_article'),
    path('new_article', views.new_article, name='new_article'),
    path('search_news', views.search_news, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    # path('pagination', views.pagination, name='pagination')
]
