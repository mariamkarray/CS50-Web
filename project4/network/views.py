from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from .models import User, Post
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class PostForm(ModelForm):
    class Meta:
        ordering = ['-created_at']
        model = Post
        fields = ('body',)
        labels = {
            'body': ''
        }
        widgets = {
            'body' : forms.Textarea(attrs={'class':'form-control', 'rows' : '3' ,'placeholder':"What's happening?"})
        }


def index(request):
    currentUser = request.user
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = currentUser
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = PostForm
    
    return render(request, "network/index.html", {
        "posts" : Post.objects.all(),
        "form" : form
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
