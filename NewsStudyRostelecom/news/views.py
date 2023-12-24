from django.shortcuts import render, HttpResponse
from .models import *
from django.db import connection, reset_queries

# для просмотра всех сообщений
def index(request):

    # получаем список авторов
    author_list = User.objects.all()
    # получаем список тэгов
    tag_list = Tag.objects.all().values('title')
    selected_author = 0
    selected_tag = 0
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        if selected_author == 0:
            # применена обратная сортировка по дате.
            articles = Article.objects.all().order_by('-date')

        else:
            # применена фильтрация по автору.
            articles = Article.objects.filter(author=selected_author)
    else:
        # применена обратная сортировка по дате.
        articles = Article.objects.all().order_by('-date')

    context = {'articles': articles, 'author_list': author_list, 'selected_author': selected_author}
    return render(request,'news/index.html', context)

# для отображения полного сообщения
def detail(request, id):
    article = Article.objects.filter(id=id).first()
    context = {'article': article}
    return render(request, 'news/news_detail.html', context)

