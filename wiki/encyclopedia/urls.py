from django.urls import include, path, reverse
# from the current directory 
from . import views

urlpatterns = [
    # when someone visits the default route, run the index function (one of my views)
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newpage", views.newPage, name="newPage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random"),
]
