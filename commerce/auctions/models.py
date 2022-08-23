from distutils.command import upload
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.db import models

class AuctionListing(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    bid = models.IntegerField()
    image =  models.ImageField(null=True, blank=True, upload_to="images/")
    numBids = models.IntegerField( default=0, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class User(AbstractUser):
   listings = models.ManyToManyField(AuctionListing, blank=True, related_name="users")
   def __str__(self):
        return self.username

class Bids(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE )
    value = models.IntegerField()
    listing = models.ForeignKey(AuctionListing,  on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} bid {self.value}$ on {self.listing}"


class Comments(models.Model):
    pass