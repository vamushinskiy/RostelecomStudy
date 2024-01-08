from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import *
from .forms import *
from .forms import AccountUpdateForm, UserUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from news.models import Article
from django.core.paginator import Paginator


def index(request):
    user_acc = Account.objects.get(user=request.user)

    return HttpResponse('Приложение Users')

#
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
            user = form.save()
            category = request.POST['account_type']
            if category == 'author':
                group = Group.objects.get(name='Actions Required')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Reader')
                user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = Account.objects.create(user=user, nickname=user.username)

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Пользователь {username} зарегистрирован!')
            return redirect('profile')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)

def profile(request):
    context = dict()
    return render(request, 'users/profile.html', context)


# Функция редактирования профиля.
def profile_edit(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, "Профиль изменён.")
            return redirect('profile')
    else:
        context = {'account_form':AccountUpdateForm(instance=account),
                       'user_form':UserUpdateForm(instance=user)}
    return render(request, 'users/edit_profile.html', context)

def password_edit(request):
    user = request.user
    form = PasswordChangeForm(user,request.POST)
    if request.method == 'POST':
        if form.is_valid():
            password_info = form.save()
            update_session_auth_hash(request,password_info)
            messages.success(request,'Пароль изменен')
            return redirect('profile')

    context = {"form": form}
    return render(request,'users/password_edit.html',context)


# Функция добавления в избранное
@login_required
def add_to_favorites(request, id):
    article = Article.objects.get(id=id)
    # Проверям есть ли такая закладка с этой новостью
    bookmark = FavoriteArticle.objects.filter(user=request.user.id,
                                              article=article)
    if bookmark.exists():
        # Если новость есть, удаляем из избранного
        bookmark.delete()
        messages.warning(request,f"Новость {article.title} удалена из закладок")
    else:
        # Если новости нет,  избранного
        bookmark = FavoriteArticle.objects.create(user=request.user, article=article)
        messages.success(request,f"Новость {article.title} добавлена в закладки")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def my_news(request):

    # получаем автора
    author = User.objects.get(id=request.user.id)
    # Получаем список категорий.
    categories = Article.categories
    articles = Article.objects.filter(author=author).order_by('-date')

    # получаем список тэгов
    # tag_list = Tag.objects.all().values('title')
    # selected_tag = 0

    if request.method == "POST":
        selected_category = int(request.POST.get('category_filter'))

        if selected_category != 0:
            articles = articles.filter(category__icontains=categories[selected_category-1][0]).order_by('-date')
    else:
        selected_category = 0
    total = len(articles)
    p = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'categories':categories, 'total': total,
               'selected_category': selected_category,}
    return render(request,'users/my_news.html', context)