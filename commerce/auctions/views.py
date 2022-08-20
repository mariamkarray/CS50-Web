from cProfile import label
from logging import PlaceHolder
from tkinter import Widget
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
import auctions
from .models import User, AuctionListing

class ListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = "__all__"
        labels = {
            'title': '',
            'description': '',
            'bid': '',
            'image': 'Image: (optional)'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}),
            'bid': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Starting Bid'})
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

def listing(request):
    # variable fot tracking if the form was submitted or not
    submitted = False
    if request.method == "POST":
        # request.POST takes whatever was in the input and passes it to the form
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
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
        'submitted' : submitted
    })
