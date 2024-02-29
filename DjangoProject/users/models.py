from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    photo = models.ImageField(upload_to='users/%y/%m/%d/', blank = True, null = True, verbose_name='Фотография')
