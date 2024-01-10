from django.shortcuts import render
from django.shortcuts import redirect
from .models import News, Product
from django.http import HttpResponse
from news.models import Article, Tag
from users.models import *

# Create your views here.

def index(request):
    # получение всех тэгов
    # articles = Article.objects.all()
    # for a in articles:
    #     print(a.title, a.tags.all())
    articles = Article.objects.prefetch_related('tags').all()
    # print(articles)
    # for a in articles:
    #     print(a.title, a.tags.all())

    tag_list = Tag.objects.all().values('title')
    # print(tag_list)
    # for t in tag_list:
    #     print(t['title'])

    author_list = User.objects.all()
    # print(author_list)

    # Отображение последней новости.
    article = Article.objects.all().order_by('-date').first()

    context = {'article': article}
    return render(request, 'main/index.html', context)

def news(request):
    return render(request,'news/index.html')



def about(request):
    return render(request,'main/about.html')

def contacts(request):
    return render(request,'main/contacts.html')

def content(request):
    return render(request,'main/content.html')

def sidebar(request):
    return render(request,'main/sidebar.html')

def custom_404(request, exception):
    # return render(request,'main/custom_404.html' )
    return HttpResponse(f'Беда! Нет страницы.:{exception}')