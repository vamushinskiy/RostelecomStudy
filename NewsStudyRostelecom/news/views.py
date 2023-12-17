from django.shortcuts import render, HttpResponse
from .models import *
from django.db import connection, reset_queries

# для просмотра всех сообщений
def index(request):
    # фильтр по автору
    author_list = User.objects.all()
    selected = 0
    if request.method == "POST":
        selected = int(request.POST.get('author_filter'))
        if selected == 0:
            # применена обратная сортировка по дате.
            articles = Article.objects.all().order_by('-date')
        else:
            # применена фильтрация по автору.
            articles = Article.objects.filter(author=selected)
    else:
        # применена обратная сортировка по дате.
        articles = Article.objects.all().order_by('-date')
    context = {'articles': articles, 'author_list': author_list, 'selected': selected}
    return render(request,'news/index.html', context)

# для отображения полного сообщения
def detail(request, id):
    article = Article.objects.filter(id=id).first()
    context = {'article': article}
    return render(request, 'news/news_detail.html', context)

