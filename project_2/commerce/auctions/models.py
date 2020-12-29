from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    listing = models.CharField(max_length=128)
    description = models.TextField()
    