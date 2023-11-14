from django.shortcuts import render
from .models import News, Product
from django.http import HttpResponse

# Create your views here.

def index(request):

    # value = 10
    # n1 = News('Новость 1', 'Текст 1', '10.11.2023')
    # n2 = News('Новость 2', 'Текст 2', '09.11.2023')
    # l = [n1, n2]
    #
    # context = {'title': 'Страница главная',
    #            'Header1': 'Заголовок страницы',
    #            'value': value,
    #            'numbers': l, }
    if request.method == 'POST':
        print('получили ПОСТ запрос!')
        print(request.POST)
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product(title, float(price), int(quantity))
        print('Создан товар: ', new_product.title, 'Общая сумма: ', new_product.amount())

    else:
        print('получили ГЕТ запрос!')

    water = Product('Кука', 45, 2)
    chocolete = Product('шоколадка', 86, 1)

    colors = ['red', 'blue', 'green', 'black']
    context = {
        'colors': colors,
        'water': water,
        'chocolate': chocolete,

    }

    return render(request,'main/index.html', context)

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
    return render(request,'main/about.html' )

def contacts(request):
    return render(request,'main/contacts.html' )

def content(request):
    return render(request,'main/content.html' )

def custom_404(request, exception):
    # return render(request,'main/custom_404.html' )
    return HttpResponse(f'Беда!:{exception}')