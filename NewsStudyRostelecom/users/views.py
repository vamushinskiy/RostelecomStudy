from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib import messages

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

# Функция регистрации нового пользователя.
def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            authenticate(username=username, password=password)
            messages.success(request, f'{username} был зарегистрирован!')
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


