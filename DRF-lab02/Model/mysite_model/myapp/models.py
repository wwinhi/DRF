from django.db import models
import datetime
from django.utils.text import slugify

class Person(models.Model):
    first_name = models.CharField(max_length=50, default='John')
    last_name = models.CharField(max_length=50, default='Witch')
    birth_date = models.DateField(default=datetime.date(2000, 1, 1))  # Sử dụng trực tiếp DateField

    def baby_boomer_status(self):
        "Returns the person's baby-boomer status."
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    @property
    def full_name(self):
        "Returns the person's full name."
        return f"{self.first_name} {self.last_name}"
    
class NewManager(models.Manager):
    # ...
    pass

class MyPerson(Person):
    objects = NewManager()
    class Meta:
        proxy = True

    def do_something(self):
        # ...
        pass

class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

class Runner(models.Model):
    MedalType = models.TextChoices("MedalType", "GOLD SILVER BRONZE")
    name = models.CharField(max_length=60)
    medal = models.CharField(blank=True, choices=MedalType, max_length=10)

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)

class Topping(models.Model):
    name = models.CharField(max_length=100)

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    toppings = models.ManyToManyField(Topping)

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    slug = models.TextField()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        if (
            update_fields := kwargs.get("update_fields")
        ) is not None and "name" in update_fields:
            kwargs["update_fields"] = {"slug"}.union(update_fields)
        super().save(**kwargs)

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ["name"]


class Unmanaged(models.Model):
    class Meta:
        abstract = True
        managed = False


class Student(CommonInfo, Unmanaged):
    home_group = models.CharField(max_length=5)

    class Meta(CommonInfo.Meta, Unmanaged.Meta):
        pass

class Place(models.Model):
    name = models.CharField(max_length=50, help_text="Tên")
    address = models.CharField(max_length=80, help_text="Địa chỉ")

    def __str__(self):
        return self.name

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False, help_text="hotdog?")
    serves_pizza = models.BooleanField(default=False, help_text="pizza?")

    place_ptr = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.name} (Restaurant)"
    
class Supplier(Place):
    customers = models.ManyToManyField(Place, related_name='providers', help_text="nhà cung cấp")

    def __str__(self):
        return f"{self.name} (Supplier)"