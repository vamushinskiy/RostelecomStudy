from django.shortcuts import render, HttpResponse
from .models import *

# для просмотра всех сообщений
def index(request):
    articles = Article.objects.all()
    context = {'articles':articles}
    return render(request,'news/index.html', context)

# для отображения полного сообщения
def detail(request, id):
    article = Article.objects.filter(id=id).first()
    context = {'article': article}
    return render(request, 'news/news_detail.html', context)

