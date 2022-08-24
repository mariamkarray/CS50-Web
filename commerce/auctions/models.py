from distutils.command import upload
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.db import models

# This class is made to avoid hard coding each category
# instead we'll make a new model so we can add/edit/delete thos categories in the future
class Categories(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    bid = models.IntegerField()
    image =  models.ImageField(null=True, blank=True, upload_to="images/")
    numBids = models.IntegerField( default=0, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    category = models.CharField(max_length=64)

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
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=64, blank=True)
    text = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.listing.title, self.name)