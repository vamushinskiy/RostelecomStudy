from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.conf import settings
import json
from users.utils import check_group
from .utils import ViewCountMixin
from django.core.paginator import Paginator

# для просмотра всех сообщений
def index(request):

    # получаем список авторов
    author_list = User.objects.all()
    # Получаем список категорий.
    categories = Article.categories
    # # получаем список тэгов
    # tag_list = Tag.objects.all().values('title')
    # selected_author = 0
    # selected_category = 0
    # selected_tag = 0
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
    #     if selected_author == 0:
    #         # применена обратная сортировка по дате.
    #         articles = Article.objects.all().order_by('-date')
    #
    #     else:
    #         # применена фильтрация по автору.
    #         articles = Article.objects.filter(author=selected_author).order_by('-date')
    #     if selected_category != 0:
    #         articles = articles.filter(category__icontains=categories[selected_category-1][0]).order_by('-date')
    # else:
    #     # применена обратная сортировка по дате.
    #     articles = Article.objects.all().order_by('-date')
    #

        request.session['author_filter'] = selected_author
        request.session['category_filter'] = selected_category
        if selected_author == 0: #выбраны все авторы
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected_author)
        if selected_category != 0: #фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category-1][0])
    else: #если страница открывется впервые или нас переадресовала сюда функция поиск
        value = request.session.get('search_input') #вытаскиваем из сессии значение поиска
        if value != None: #если не пустое - находим нужные ноновсти
            articles = Article.objects.filter(title__icontains=value)
            # del request.session['search_input'] #чистим сессию, чтобы этот фильтр не "заело"
        else: #если это не поисковый запрос, а переход по пагинатору или первое открытие
            selected_author = request.session.get('author_filter')
            selected_category = request.session.get('category_filter')
            articles = Article.objects.all()
            if selected_author != None and int(selected_author) != 0:  # если не пустое - находим нужные ноновсти
                articles = articles.filter(author=selected_author)
            else:
                selected_author = 0
            if selected_category != None and int(selected_category) != 0:  # фильтруем найденные по авторам результаты по категориям
                articles = articles.filter(category__icontains=categories[selected_category - 1][0])
            else:
                selected_category = 0

    #сортировка от свежих к старым новостям
    articles=articles.order_by('-date')
    total = len(articles)
    p = Paginator(articles,3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    title = ('Заголовок страницы новости-индекс')
    context = {'articles': page_obj, 'author_list':author_list, 'selected_author':selected_author,
               'categories':categories,'selected_category': selected_category, 'total':total,
               'title':title
               }

    return render(request,'news/index.html', context)


# Используем декоратор проверки аутентификации.
@login_required(login_url=settings.LOGIN_URL)
# Применяем декоратор
@check_group('Authors')
# Функция создания нового сооющения.
def new_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
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
                # Сохраняем тэги
                form.save_m2m()
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=create_article, image=img, title=img.name)
                # Очищаем форму.
                #form = ArticleForm()
                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request, 'news/new_article.html', {'form':form})


# Используем дженерик для отображения полного сообщения
class ArticleDetailView(ViewCountMixin,DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

    # Для отображения картинок в новости добавляем метод:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['images'] = images
        return context

# Используем дженерик для редактирования сообщения
class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/new_article.html'
    fields = ['title', 'anouncement', 'text', 'date', 'tags']

   # Используем дженерик для удаления сообщения
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_index')
    template_name = 'news/delete_article.html'


# функция поиска
def search(request):
    # Если так не сработает, то делаем как ниже
    #if request.is_ajax():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        articles = Article.objects.filter(title__icontains=q)
        results = []
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetypes = 'aplication/json'
    return HttpResponse(data, mimetypes)




