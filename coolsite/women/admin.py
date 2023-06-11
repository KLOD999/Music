import unittest
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):   # добавление дополнительных полей в admin-панели
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)  # редактирование записей (опубликовано или нет)
    list_filter = ('is_published', 'time_create')  # фильтрация с правой стороны
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update') # редактируемые поля
    readonly_fields = ('time_create', 'time_update', 'get_html_photo') # нередактируемые поля
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        else:
            return "Нет фото"

    get_html_photo.short_description = "Миниатюра"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # записывать запятую в конце надо, т.к. передается кортеж, а если оставить без запятой,
                               # то будет строка
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

# изменить сам заголовок «Администрирование Django»
admin.site.site_title = 'Админ-панель сайта о музыкальных альбомах'
admin.site.site_header = 'Админ-панель сайта о музыкальных альбомах'
