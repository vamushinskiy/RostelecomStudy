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
from .utils import check_group


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
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)

def profile(request):
    context = dict()
    return render(request, 'users/profile.html', context)


# Функция редактирования профиля.
@login_required
def profile_edit(request):
    user = request.user
    account = Account.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        context = {'account_form': AccountUpdateForm(instance=account),
                   'user_form': UserUpdateForm(instance=user)}
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, "Профиль изменён.")
            return redirect('profile')
        else:
            error_dict = dict(account_form.errors)
            error_dict.update(dict(user_form.errors))
            messages.warning(request, error_dict)
    else:
        context = {'account_form': AccountUpdateForm(instance=account),
                   'user_form': UserUpdateForm(instance=user)}

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


@login_required
def favorites_list(request):
    categories = Article.categories
    author_list = User.objects.all()
    favorite_articles = FavoriteArticle.objects.filter(user=request.user)
    articles = [favorite_article.article for favorite_article in favorite_articles]
    selec_author = 0
    selec_category = 0
    if request.method == "POST":
        selec_author = int(request.POST.get('author_filter'))
        selec_category = int(request.POST.get('category_filter'))
        if selec_author == 0:
            articles = Article.objects.filter().order_by('-date')
        else:
            # применена фильтрация по автору.
            articles = Article.objects.filter(author=selec_author).order_by('-date')
        if selec_category != 0:
            articles = articles.filter(category__icontains=categories[selec_category - 1][0]).order_by('-date')
    else:
        # применена обратная сортировка по дате.
        articles = Article.objects.all().order_by('-date')
    total = len(articles)
    p = Paginator(articles, 3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj,
               'author_list': author_list,
                'selec_author':selec_author,
               'categories': categories,
               'selec_category': selec_category,
               'total': total, }

    return render(request, 'users/my_favorites.html',context)


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
        request.session['selected_category'] = selected_category
        if selected_category != 0:
            articles = articles.filter(category__icontains=categories[selected_category-1][0]).order_by('-date')
    else:
        selected_category = request.session.get('selected_category')
        if selected_category != None and selected_category != 0:  # если не пустое - находим нужные ноновсти
            articles = articles.filter(category__icontains=categories[selected_category - 1][0])
    total = len(articles)
    p = Paginator(articles, 3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'categories':categories, 'total': total,
               'selected_category': selected_category,}
    return render(request,'users/my_news.html', context)

@login_required
def profile_delete(request):
    user = request.user
    user.delete()
    return redirect('news_index')


def my_favorites(request):
    categories = Article.categories  # создали перечень категорий
    author_list = User.objects.all()
    bookmarks_news = FavoriteArticle.objects.filter(user=request.user.id).values('article_id')
    articles = Article.objects.filter(id__in=bookmarks_news)
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
        request.session['selected_author'] = selected_author
        request.session['selected_category'] = selected_category
        if selected_author == 0:  # выбраны все авторы
            articles = articles.all().order_by('-date')
        else:
            articles = articles.filter(author=selected_author)
        if selected_category != 0:  # фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category - 1][0])
    else:  # если страница открывется
        selected_author = request.session.get('selected_author')
        print(selected_author)
        if selected_author != None and selected_author != 0:  # если не пустое - находим нужные новости
            articles = articles.filter(author=selected_author)
        selected_category = request.session.get('selected_category')
        print(selected_category)
        if selected_category != None and selected_category != 0:  # если не пустое - находим нужные ноновсти
            articles = articles.filter(category__icontains=categories[selected_category - 1][0])
    total = len(articles)
    p = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'total': total, 'selected_author': selected_author,
               'categories': categories, 'selected_category': selected_category, 'author_list': author_list}
    return render(request,'users/my_favorites.html',context)