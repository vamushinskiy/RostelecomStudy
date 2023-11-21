from django.shortcuts import render, HttpResponse
from .models import  *


def index(request):
    article = Article.objects.all().first()
    context = {'article':article}
    return render(request,'news/index.html', context)

def show(request):
    return render(request,'news/news.html')

def detail(request, id):
    article = Article.objects.filter(id=id)
    return HttpResponse(f'<h1>{article.title}</h1>')