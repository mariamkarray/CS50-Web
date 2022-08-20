from distutils.command import upload
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    bid = models.IntegerField()
    image =  models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.title

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass