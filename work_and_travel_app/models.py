from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Grade(models.Model):
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=255)


class Answer(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)


class BaseInformation(models.Model):
    SEX_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    contact_number = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField()
    are_you_traveling = models.BooleanField(default=False)
    native_origin = models.CharField(max_length=255)
    sex = models.CharField(max_length=9, choices=SEX_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Offer(models.Model):
    OFFER_CHOICES = [
        ('job offer', 'Job Offer'),
        ('job seekers', 'Job Seekers'),
    ]

    name = models.CharField(max_length=255)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    description = models.TextField()
    offer_type = models.CharField(max_length=20, choices=OFFER_CHOICES)
    category = models.ManyToManyField(Category)
    since_when = models.DateField()
    until_when = models.DateField()
    only_for_women = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Message(models.Model):
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
