from distutils.command import upload
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.db import models

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    bid = models.IntegerField()
    image =  models.ImageField(null=True, blank=True, upload_to="images/")
    numBids = models.IntegerField()

    def __str__(self):
        return self.title

class User(AbstractUser):
   listings = models.ManyToManyField(AuctionListing, blank=True, related_name="users")
   def __str__(self):
        return self.username

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass