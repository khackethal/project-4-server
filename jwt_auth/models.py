from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=250)
    cover_photo = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=250, blank=True)
    user_city = models.CharField(max_length=50)
    user_country = models.CharField(max_length=50)


def __str__(self):
    return f'{self.firstname} {self.lastname}'


