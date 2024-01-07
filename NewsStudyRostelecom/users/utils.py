from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages

# Создание декоратора
def check_group(*groups):
    def decorator(function):
        # Функция "обёртка"
        def wrapper(request,*args,**kwargs):
            user = request.user
            # если есть группы у нашего пользователя
            if user.groups.filter(name__in=groups).exists():
                # то выполняется функция "конфетка"
                return function(request,*args,**kwargs)
            messages.warning(request,'У Вас нет доступа сюда.')
            # перенаправляем пользователя туда, откуда он пришёл
            return HttpResponseRedirect(request.POST.get('next','/'))
        return wrapper
    return decorator