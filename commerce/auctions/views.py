from cProfile import label
from logging import PlaceHolder
from tkinter import Widget
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
import auctions
from .models import User, AuctionListing, Bids, Categories, Comments
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

categories = list(Categories.objects.all().values_list('name', 'name'))

class ListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ('title', 'category', 'description', 'bid', 'image')
        
        labels = {
            'title': '',
            'category': '',
            'description': '',
            'bid': '',
            'image': 'Image: (optional)'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
            'category': forms.Select(choices=categories),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
            'bid': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Bid'})
        }
        owner = forms.IntegerField(disabled=True) 
        
class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ('value',)
        labels = {
            'value': '',
        }
        widgets = {
            'value': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Bid'})
        }
class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
        labels = {
                'text': ''
            }
        widgets = {
                'text': forms.Textarea(attrs={'class':'form-control', 'placeholder':'What is on your mind?'}),
            }

def index(request):
    return render(request, "auctions/index.html", {
        "listings" : AuctionListing.objects.all()
    })
def login_view(request):
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="auctions:login")
def listing(request):
    # variable for tracking if the form was submitted or not
    submitted = False
    # getting ID of the current user
    currentUser = request.user
    if request.method == "POST":
        # request.POST takes whatever was in the input and passes it to the form
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = currentUser
            form.save()
            # redirect back to the page itself
            return HttpResponseRedirect('/listing?submitted=True')
    else:
        form = ListingForm
        # the responseRedirect passes the submitted variable into the get request 
        # if it did that that means the user submitted the form
        if 'submitted' in request.GET:
            submitted = True     

    return render(request, "auctions/listing.html", {
        "form" : form,
        'submitted' : submitted,
        "userID" : currentUser.id
    })
def listing_page(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    currentUser = request.user
    if listing.closed:
        winner = False
        if listing.numBids > 0:
            for bids in Bids.objects.all():
                highestBid = Bids.objects.filter(listing=listing_id).order_by('-value').first()
                highestBidUser = highestBid.user.id
            if currentUser.id == highestBidUser:
                winner = True
            return render(request, "auctions/listing-page.html", {
                            "listing" : listing,
                            "closed": True,
                            "winner": winner,
                            "user": currentUser
            })

    else:    
        if request.method == "POST" and "bid" in request.POST:
            form = BidForm(request.POST)
            form.instance.user = currentUser
            form.instance.listing = listing
            if form.is_valid():
                    bid = form.cleaned_data["value"]
                    if bid < listing.bid:
                        messages.error(request,"The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed!") 
                        return redirect("/listing/%s" % listing_id)   
                    else:
                        listing.numBids+=1
                        listing.bid = bid
                        form.instance.value = bid
                        listing.save()
                        form.save()
                        return redirect("/listing/%s" % listing_id)    
    # adding a comment
        elif request.method == "POST" and "comment" in request.POST:
            commentForm = CommentForm(request.POST)
            commentForm.instance.name = currentUser
            commentForm.instance.listing = listing
            if commentForm.is_valid():
                text =  commentForm.cleaned_data["text"]
                commentForm.instance.text = text
                commentForm.save()
                return redirect("/listing/%s" % listing_id)        
                    
        form = BidForm()
        commentForm = CommentForm()
        # checking if the listing is currently in the users's watchlist
        found = False
        if request.user.is_authenticated:
            listing = AuctionListing.objects.get(pk=listing_id)
            user = User.objects.get(pk=currentUser.id)
            user_listings =  user.listings.all()
            if listing in user_listings:
                found = True
        # listingOwner can close listing
        listingOwner = listing.owner
        canClose = False
        if currentUser == listingOwner:
            canClose = True
        return render(request, "auctions/listing-page.html", {
                "listing" : listing,
                "form": form,
                "found": found,
                "canClose": canClose,
                "commentForm": commentForm
            })
        


@login_required
def watchlist(request,  user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/watchlist.html", {
        "user" : user,
        "listings": user.listings.all()
    })

def addToWatchlist(request, listing_id):
    currentUser = request.user
    listing = AuctionListing.objects.get(pk=listing_id)
    user = User.objects.get(pk=currentUser.id)
    user_listings =  user.listings.all()
    if listing in user_listings:
        user.listings.remove(listing)
        return render(request, "auctions/watchlist.html", {
        "user" : user,
        "listings": user.listings.all()
        })
    user.listings.add(listing)
    user.save()
    return render(request, "auctions/watchlist.html", {
        "user" : user,
        "listings": user.listings.all(),
        "found" : True
    })

def closeListing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.closed = True
    listing.save()
    return render(request, "auctions/listing-page.html", {
                "listing" : listing,
                "closed" : True
            })
# categories list
def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
#individual category view
def categoryView(request, cat):
    category_listings = AuctionListing.objects.filter(category=cat)
    return render(request, "auctions/categoryView.html",
    {
        'category': cat,
        'category_listings': category_listings
        
    })
