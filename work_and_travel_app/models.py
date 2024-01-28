from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    index = models.CharField(max_length=4, unique=True)


class Grades(models.Model):
    rating = models.IntegerField()
    description = models.CharField(max_length=255)


class BaseInformation(models.Model):
    SEX_CHOICES = [
        ('kobieta', 'Kobieta'),
        ('mężczyzna', 'Mężczyzna'),
        ('inne', 'Inne'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField()
    are_you_traveling = models.BooleanField(default=False)
    country = models.CharField(max_length=255)
    sex = models.CharField(max_length=9, choices=SEX_CHOICES)
    # grades = models.ForeignKey(Grades, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.first_name} {self.last_name}"


class Announcement(models.Model):
    OFFER_CHOICES = [
        ('employer', 'Pracodawca'),
        ('employee', 'Pracownik'),
    ]

    name = models.CharField(max_length=50)
    big_city_100_km = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    description = models.TextField()
    offer_type = models.CharField(max_length=20, choices=OFFER_CHOICES)
    category = models.ManyToManyField(Category)
    since_when = models.DateTimeField()
    until_when = models.DateTimeField()
    only_for_women = models.BooleanField(default=False)
    who = models.ForeignKey(BaseInformation, on_delete=models.CASCADE)


class Message(models.Model):
    message = models.TextField()
