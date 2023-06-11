# файл для миксинов (помогают избегать дублирования кода в приложении)
from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить альбом", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3  # отображение 3 записей на 1 стр

    def get_user_context(self, **kwargs): # формирует контекст для шаблона ( по умолчанию)
        context = kwargs  # сформирован начальный словарь из параметров, переданных функции
        cats = cache.get('cats')   # выборка категорий из кэша с помощью функции get()
        if not cats:
            cats = Category.objects.annotate(Count('women'))
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context