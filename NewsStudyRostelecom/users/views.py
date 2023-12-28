from django.shortcuts import render, HttpResponse
from .models import *
from .forms import *

def index(request):
    user_acc = Account.objects.get(user=request.user)
    print(user_acc.nickname, user_acc.post, user_acc.point)
    return HttpResponse('Приложение Users')

def contact_page(request):
    if request.method =="POST":
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'users/contact_page.html', context)
