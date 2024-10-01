from datetime import date
from django.db.models import Value, JSONField
from django.db import models
from django.db.models import Q
from django.db.models import Aggregate, IntegerField
from django.db.models.fields import Field

class Blog(models.Model):
    name = models.CharField(max_length=100, default='Default Blog Name')
    tagline = models.TextField(default='Default tagline')

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200, default='Default Author Name')
    email = models.EmailField(default='author@example.com')

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE,
        default=1  # Giả sử Blog với id=1 là blog mặc định
    )
    headline = models.CharField(max_length=255, default='Default Headline')
    body_text = models.TextField(default='Default body text.')
    pub_date = models.DateField(default=date.today)
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)  # Không thể đặt default trực tiếp
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline

class Dog(models.Model):
    name = models.CharField(max_length=200, default='Default Dog Name')
    data = models.JSONField(null=True, default=dict)

    def __str__(self):
        return self.name
    
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateField()

    def __str__(self):
        return self.question

class ThemeBlog(Blog):
    theme = models.CharField(max_length=100, default='default_theme')

    def __str__(self):
        return f"{self.name} - {self.theme}"
    
class EntryManager(models.Manager):
    def is_published(self):
        return self.filter(pub_date__lte=date.today())


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    objects = models.Manager()
    entries = EntryManager()

class EntryDetail(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    details = models.TextField()
    
class Count(Aggregate):
    function = 'COUNT'
    template = '%(function)s(%(distinct)s%(expressions)s)'
    allow_distinct = True
    name = 'Count'
    output_field = IntegerField()

    def __init__(self, expression, distinct=False, **extra):
        super().__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=self.output_field,
            **extra
        )

class Event(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
    )
    date = models.DateField()

class City(models.Model):
    # ...
    pass


class Person(models.Model):
    # ...
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


class Book(models.Model):
    # ...
    author = models.ForeignKey(Person, on_delete=models.CASCADE)

class Topping(models.Model):
    name = models.CharField(max_length=30)


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )
    
class Restaurant(models.Model):
    pizzas = models.ManyToManyField(Pizza, related_name="restaurants")
    best_pizza = models.ForeignKey(
        Pizza, related_name="championed_by", on_delete=models.CASCADE
    )

class CommonlyUsedModel(models.Model):
    f1 = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "app_largetable"


class ManagedModel(models.Model):
    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)

    class Meta:
        db_table = "app_largetable"

class Chapter(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=256, default="Untitled Book")
    chapters = models.ManyToManyField(
        Chapter,
        through='BookChapter',
        related_name='books',
        help_text="Danh sách các chương thuộc về cuốn sách này."
    )

    def __str__(self):
        return self.title


class BookChapter(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='book_chapters',
        help_text="Liên kết đến cuốn sách."
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='book_chapters',
        help_text="Liên kết đến chương."
    )

    class Meta:
        unique_together = ('book', 'chapter')  # Đảm bảo mỗi cặp book-chapter là duy nhất
        verbose_name = 'Book Chapter'
        verbose_name_plural = 'Book Chapters'

    def __str__(self):
        return f"{self.book.title} - Chapter {self.order}: {self.chapter.title}"