from django.shortcuts import render, HttpResponse
from .models import *

def index(request):
    user_acc = Account.objects.get(user=request.user)
    print(user_acc.nickname, user_acc.post, user_acc.point)
    return HttpResponse('Приложение Users')
