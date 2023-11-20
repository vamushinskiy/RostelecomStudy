from django.shortcuts import render
from django.shortcuts import redirect
from .models import News, Product
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def news(request):
    return render(request,'main/news.html')

def get_demo(request, a, operation, b):
    #match operation:
        # case 'plus':
        #     result = int(a) + int(b)
        # case 'minus':
        #     result = int(a) - int(b)
        # case 'multiply':
        #     result = int(a) * int(b)
        # case 'devide':
        #     result = int(a) / int(b)

    return HttpResponse(f'Вы ввели: {a} и {b} <br> Результат {operation}: ')


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