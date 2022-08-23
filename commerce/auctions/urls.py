from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path("listing/<listing_id>", views.listing_page, name="listing-page"),
    path("watchlist/<user_id>", views.watchlist, name="watchlist"),
    path("add_to_watch_list/<listing_id>", views.addToWatchlist, name="addToWatchlist"),
    path("close_listing/<listing_id>", views.closeListing, name="close-listing")
]
