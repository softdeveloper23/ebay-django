from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ListingForm
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
        active_listings = Listing.objects.all()  # Assuming all listings are active for simplicity
        return render(request, "auctions/index.html", {'listings': active_listings})

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

# Create a listing
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.user = request.user
            new_listing.save()
            return redirect('index')
    else:
        form = ListingForm()
    return render(request, 'auctions/create-listing.html', {'form': form})

# View a listing
# View a listing
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    user_watchlist_ids = []
    if request.user.is_authenticated:
        user_watchlist_ids = Watchlist.objects.filter(user=request.user).values_list('listing_id', flat=True)
    return render(request, 'auctions/listing-detail.html', {
        'listing': listing,
        'user_watchlist_ids': user_watchlist_ids
    })

# Add a listing to a watchlist
@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    Watchlist.objects.get_or_create(user=request.user, listing=listing)
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))

# Remove a listing from a watchlist
@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    Watchlist.objects.filter(user=request.user, listing=listing).delete()
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))

# View a user's watchlist
@login_required
def watchlist(request):
    user_watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist': user_watchlist})
