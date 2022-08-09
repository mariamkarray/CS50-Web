from django.urls import include, path, reverse
# from the current directory 
from . import views

urlpatterns = [
    # when someone visits the default route, run the index function (one of my views)
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("<str:title>", views.entry, name="entry")
]
