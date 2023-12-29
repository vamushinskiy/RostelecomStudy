from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

# для просмотра всех сообщений
def index(request):

    # получаем список авторов
    author_list = User.objects.all()
    # Получаем список категорий.
    categories = Article.categories
    # получаем список тэгов
    tag_list = Tag.objects.all().values('title')
    selected_author = 0
    selected_category = 0
    selected_tag = 0
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        if selected_author == 0:
            # применена обратная сортировка по дате.
            articles = Article.objects.all().order_by('-date')

        else:
            # применена фильтрация по автору.
            articles = Article.objects.filter(author=selected_author)
    else:
        # применена обратная сортировка по дате.
        articles = Article.objects.all().order_by('-date')

    context = {'articles': articles, 'author_list': author_list, 'selected_author': selected_author, 'categories':categories}
    return render(request,'news/index.html', context)

# для отображения полного сообщения
# def detail(request, id):
#     article = Article.objects.filter(id=id).first()
#     context = {'article': article}
#     return render(request, 'news/news_detail.html', context)

# Используем декоратор проверки аутентификации.
@login_required(login_url="/")
# Функция создания нового сооющения.
def new_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            # Проверяем пользователя
            current_user = request.user

            # Если не аноним
            if current_user.id != None:
                # Создаём экземпляр сообщения не сохраняя в БД.
                create_article = form.save(commit=False)
                # то добавляем его к новости
                create_article.author = current_user
                # И сохраняем новость.
                create_article.save()
                form.save_m2m()
                # Очищаем форму.
                form = ArticleForm()
                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request, 'news/new_article.html', {'form':form})


# Используем дженерик для отображения полного сообщения
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

# Используем дженерик для редактирования сообщения
class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/new_article.html'
    fields = ['title', 'anouncement', 'text', 'date', 'tags']

    # Используем дженерик для редактирования сообщения
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_index')
    template_name = 'news/delete_article.html'
