from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User


class Genre(models.Model):
    """
    Модель, представляющая книжный жанр (например, научная фантастика, нехудожественная литература).
    """
    name = models.CharField(max_length=200, help_text="Введите жанр книги(Научная фантастика, детектив")

    def __str__(self):
        """
        Строка для представления объекта модели (на сайте администратора и т.д.)
        """
        return self.name


class Language(models.Model):
    """Модель, представляющая язык (например, английский, французский, японский и т.д.)"""
    name = models.CharField(max_length=200,
                            help_text="Введите язык, на котором написана книга(Английский, русский и т.д.")

    def __str__(self):
        """Строка для представления объекта модели (на сайте администратора и т.д.)"""
        return self.name


class Book(models.Model):
    """
    Модель, представляющая книгу (но не конкретную копию книги).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Первичный ключ используется, потому что у книги может быть только один автор,
    # но у авторов может быть несколько книг
    # Автор как строка, а не объект, потому что он еще не был объявлен в файле.
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField используется, потому что жанр может содержать много книг.
    # Книги могут охватывать многие жанры.
    # Класс жанра уже определен, поэтому мы можем указать объект выше.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        """Создает строку для жанра. Это необходимо для отображения жанра в Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def display_genre(self):
        """
        Создает строку для жанра. Это необходимо для отображения жанра в Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return self.title


    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к определенному экземпляру книги.
        """
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
    Модель, представляющая конкретную копию книги (т. е. которую можно позаимствовать из библиотеки).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный идентификатор для этой конкретной книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Статус книги')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):
        """
        Строка для представления объекта модели
        """
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """
    Модель, представляющая автора.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("can_change", "Delete/change/add author"),)


    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к определенному экземпляру автора.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return '{0}, {1}'.format(self.last_name, self.first_name)

