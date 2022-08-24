from django.contrib import admin
from .models import AuctionListing, Bids, Comments, User, Categories
# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Bids)
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Comments)
