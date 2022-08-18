from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    bid = models.IntegerField(max_length=10000)
    image =  models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass