from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import *
from .models import *
from .utils import *


# def index(request):
# return HttpResponse('Главная страница')

# def categories(request, catid):
# if (request.GET):  #В консоле отображаются результаты GET запроса в виде "ключ-значение"
# print(request.GET)

# return HttpResponse(f'<h1>Статьи по категориям</h1><p>{catid}</p>')

def archive(request, year):
    if 2020 < int(year) < 2030:  # Обработка исключения 404 (переход на ошибку 404 ->
        return redirect('home', permanent=True)  # отображение функции pageNotFound с результатом "Страница не найдена"
    if int(year) > 2030:
        raise Http404

    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound(f'<h1>Страница не найдена</h1>')


# menu = [{'title': "О сайте", 'url_name': 'about'},    переносим меню в файл utils
# {'title': "Добавить статью", 'url_name': 'add_page'},
# {'title': "Обратная связь", 'url_name': 'contact'},
# {'title': "Войти", 'url_name': 'login'}
# ]


# def index(request):
# posts = Women.objects.all()
##cats = Category.objects.all()

# context = {
# 'posts': posts,
##'cats': cats,
# 'menu': menu,
# 'title': 'Главная страница',
# 'cat_selected': 0,
# }

# return render(request, 'women/index.html', context=context)
##   return render(request, 'women/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'})

# передача аргумента в виде словаря (3 атрибут)
# передача из списка menu на главную страницу (отобразить элементы меню в виде списка),
# в index.html передается цикл for где перебираются элементы из menu (список передан выше на 25 строке)


#  во фреймворке Django помимо функций можно использовать и классы представлений (контроллеры классов):
# CBV – Class-Based Views
# создадим функцию index через класс:
class WomenHome(DataMixin, ListView):
    model = Women  # отображение статей, которые находятся в модели women
    template_name = 'women/index.html'  # указание к какому шаблону перенаправить
    context_object_name = 'posts'  # отображение статей
    extra_context = {'title': 'Главная страница'}  # название вкладки(только для статических)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # обращение к базовому классу (ListView) и берем оттуда контекст
        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0 # чтобы подсвечивалась ссылка, на которой находимся
        # context['menu'] = menu  # отображение меню
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # чтобы показывать только те записи, которые отмечены как опубликованные
        return Women.objects.filter(is_published=True).select_related('cat')


def about(request):
    contact_list = Women.objects.all()

    page_number = request.GET.get('page')
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


# передача аргумента в виде словаря (3 атрибут)

# эти аргументы будут передаваться в шаблоны index.html и about.html в {{ title }}

# сейчас имеются два файла index.html и about.html в которых передана почти одна и та же информация
# нарушается принцип DRY, поэтому создается базовый шаблон base.html

# в базовом шаблоне список menu, который будет отображаться на двух страницах, в других файлах
# наследование базового шаблона

# def addpage(request):
# if request.method == 'POST':
# form = AddPostForm(request.POST, request.FILES) # список файлов, которые были переданы на сервер из формы
# if form.is_valid():
##print(form.cleaned_data)
# form.save() # сохранение формы
# return redirect('home')

# else:
# form = AddPostForm()
# return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):  # LoginRequiredMixin миксин,
    form_class = AddPostForm  # который позволяет ограничить доступ к странице
    template_name = 'women/addpage.html'  # для неавторизованных пользователей
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')  # указывает адрес перенаправления для незарегистрированного пользователя
    raise_exception = True  # вместо перенаправлений, можно генерировать страницу с кодом 403 – доступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        c_def = self.get_user_context(title="Добавление альбома")
        return dict(list(context.items()) + list(c_def.items()))


# def contact(request):
# return HttpResponse("Обратная связь")

class ContactFormView(DataMixin, FormView):  # форма обратной связи
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
# return HttpResponse("Авторизация")

# def show_post(request, post_id):
# return HttpResponse(f"Отображение статьи с id = {post_id}")


# def show_post(request, post_slug):
# post = get_object_or_404(Women, slug=post_slug) # получить определенную запись из БД

# context = {
# 'post': post,
# 'menu': menu,
# 'title': post.title,
# 'cat_selected': post.cat_id,
# }
# return render(request, 'women/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = context['post']
        # context['menu'] = menu
        # return context
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_id):
# posts = Women.objects.filter(cat_id=cat_id)
# cats = Category.objects.all()

# if len(posts) == 0:
# raise Http404()

# context = {
# 'posts': posts,
##'cats': cats,
# 'menu': menu,
# 'title': 'Отображение по рубрикам',
# 'cat_selected': cat_id,
# }

# return render(request, 'women/index.html', context=context)

# cats = Category.objects.all() и 'cats': cats, убрали, т.к. повторяется в 2-ух функциях, вместо этого есть новая директория
# templatetags где есть функция, которая используется чтобы не нарушать принцип DRY

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['menu'] = menu
        # context['cat_selected'] = context['posts'][0].cat_id
        # return context
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)

        return context | c_def


class RegisterUser(DataMixin, CreateView):  # регистрация
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # ри успешной регистрации пользователя автоматически его авторизовывать
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):  # oтображение формы авторизации
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

# в Django есть понятие «ленивых» и «жадных» запросов. Ленивые, то есть, отложенные запросы, которые выполняются только
# в момент непосредственного обращения к данным, например, для вывода рубрики. Как раз здесь выполняется отложенный запрос.
# Они достаточно удобны при работе с единичными записями, но когда их много, то возникает неприятный эффект резкого
# увеличения числа SQL-запросов, что мы сейчас и наблюдаем.

# Как можно оптимизировать этот процесс? Очевидно, нужно сделать загрузку категорий и постов одним запросом.
# Для этого в Django имеются два полезных метода:

# select_related(key) – «жадная» загрузка связанных данных по внешнему ключу key, который имеет тип ForeignKey;
# prefetch_related(key) – «жадная» загрузка связанных данных по внешнему ключу key, который имеет тип ManyToManyField.

# Для более тонкой настройки и использования механизма кэширования в Django имеются весьма полезные функции,
# которые составляют уровень API для кэширования. Основные из них, следующие:

# cache.set() – сохранение произвольных данных в кэш по ключу;
# cache.get() – выбор произвольных данных из кэша по ключу;
# cache.add() – заносит новое значение в кэш, если его там еще нет (иначе данная операция игнорируется);
# cache.get_or_set() – извлекает данные из кэша, если их нет, то автоматически заносится значение по умолчанию;
# cache.delete() – удаление данных из кэша по ключу;
# cache.clear() – полная очистка кэша.
