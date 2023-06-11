# директория и файл созданы, чтобы следовать принципу DRY и избежать повторения
from django import template
from women.models import *

register = template.Library() # регистрация собственных шаблонных тегов

# Django позволяет использовать два вида пользовательских тегов:

# simple tags – простые теги;
# inclusion tags – включающие теги.

# простой тег будет загружать категории из БД и использоваться непосредственно в шаблоне

# включающий тег, позволяет дополнительно формировать свой собственный шаблон на основе некоторых данных
# и возвращать фрагмент HTML-страницы


# simple tags:                                # чтобы связать эту функцию с тегом, или, превратить эту функцию в тег
@register.simple_tag(name='getcats')   # используется специальный декоратор, доступный через переменную register
def get_categories():       # функция будет выполняться при вызове тега из шаблона
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)
    # нужны будут списки категорий


# inclusion tags:
@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):  # отображение той категории, в которой находимся
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}

