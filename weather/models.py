from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.username

