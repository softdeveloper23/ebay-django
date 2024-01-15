from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("listing/<int:listing_id>", views.listing_detail, name="listing"),
    path("add-to-watchlist/<int:listing_id>", views.add_to_watchlist, name="add-to-watchlist"),
    path("remove-from-watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove-from-watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("place-bid/<int:listing_id>", views.place_bid, name="place-bid"),
    path("close-listing/<int:listing_id>", views.close_listing, name="close-listing"),
]
