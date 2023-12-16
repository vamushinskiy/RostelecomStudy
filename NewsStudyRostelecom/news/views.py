from django.shortcuts import render, HttpResponse
from .models import *


def index(request):
    article = Article.objects.all().first()
    context = {'article':article}
    return render(request,'news/index.html', context)

# def news(request):
#     return render(request,'news/news.html')

def detail(request, id):
    # article = Article.objects.filter(id=id).first()
    # return HttpResponse(f'<h1>{article.title}</h1>')

    articles = Article.objects.all()
    s=''
    for article in articles:
        s+=f'<h1>{article.title}<h1><br>'
    return HttpResponse(s)