from django.db import models
from django.urls import reverse

class Women(models.Model): #поле id автоматически прописано в этом классе
    # verbose_name - параметр, в котором отражаются названия в admin-панели
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL") # добавление слага
    content = models.TextField(blank=True, verbose_name="Описание альбома") #blank=True - поле может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото") #доп.настройка в файле settings(MEDIA_ROOT, MEDIA_URL)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории") #внешний ключ(null=True для создания таблицы в БД)

#для работы с ORM, используется консоль shell внутри фреймворка

    def __str__(self): #выводит информацию о заголовках в консоле
        return self.title

    def get_absolute_url(self):   # т.к. имеется эта функция, в admin панели есть кнопка "смотреть на сайте"
        return reverse('post', kwargs={'post_slug': self.slug})  #2 способ динамических URL, только если связано с БД

    class Meta:        # вложенный класс для более точной работы с admin-панелью
        verbose_name = 'Музыкальные альбомы'    # замена названия в админке
        verbose_name_plural = 'Музыкальные альбомы' # чтобы убрать s от множественного числа
        ordering = ['time_create', 'title'] # порядок сортировки (если перед названием в кавычках указать минус,
                                                    # то будет обратная сортировка)


# Фреймворк Djnago имеет три специальных класса для организации связей:

# ForeignKey – для связей Many to One (поля отношений);
# ManyToManyField – для связей Many to Many (многие ко многим);
# OneToOneField – для связей One to One (один к одному).


# Класс ForeignKey принимает два обязательных аргумента:

# ссылка или строка класса модели, с которой происходит связывание (в нашем случае это класс Category – модели для категорий);
# опция on_delete, накладывающая ограничения при удалении внешней записи (в нашем примере – это удаление из таблицы Category).
# В свою очередь, опция on_delete может принимать следующие значения:

# models.CASCADE – при удалении записи из первичной модели (у нас это таблица Category) происходит
                   # удаление всех записей из вторичной модели (Women), связанных с удаляемой категорией;
# models.PROTECT – запрещает удаление записи из первичной модели, если она используется во вторичной (выдает исключение);
# models.SET_NULL – при удалении записи первичной модели устанавливает значение foreign key в NULL
                   # у соответствующих записей вторичной модели;
# models.SET_DEFAULT – то же самое, что и SET_NULL, только вместо значения NULL устанавливает значение по умолчанию,
                   # которое должно быть определено через класс ForeignKey;
# models.SET() – то же самое, только устанавливает пользовательское значение;
# models.DO_NOTHING – удаление записи в первичной модели не вызывает никаких действий у вторичных моделей.

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Жанр")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id']
