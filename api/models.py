from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Address(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.IntegerField()

    def __str__(self):
        return f'{self.city}-{self.street} {self.house_number}'


class Contact(models.Model):
    email = models.EmailField()
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
    )


class Producer(models.Model):
    name = models.CharField(max_length=50)
    contact = models.OneToOneField(
        Contact,
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField('Product')
    provider = models.ForeignKey(
        'Producer',
        on_delete=models.CASCADE,
        null=True,
    )
    level = models.IntegerField()
    debt = models.DecimalField(max_digits=14,
                               decimal_places=2,
                               validators=[MinValueValidator(float('0.0'))]
                               )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    release_date = models.DateField()

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=70)
    last_name = models.CharField(_("last name"), max_length=70)
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    producer = models.ForeignKey(
        'Producer',
        on_delete=models.CASCADE,
        null=True,
    )
