from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.db.models import Max

from .models import User, AuctionListings, Bids, Comments, Category


def index(request):
    listings = AuctionListings.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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

def listing(request, id):
    listing = AuctionListings.objects.get(pk=id)
    if request.method == "POST":
        listingBid = float(request.POST["listingBid"])
        if listingBid <= listing.startingBid:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Error: Your bid has to be greater than the starting bid"
            })
        if listingBid <= listing.bid.listingBid:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Error: Your bid has to be greater than the current bid"
            })
        bid = Bids(userBid=request.user, listingBid=float(request.POST["listingBid"]))
        bid.save()
        listing.bid = bid
        listing.save()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": None
    })

@login_required(login_url='login')
def create_view(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["startingBid"]
        imageUrl = request.POST["imageUrl"]
        categoryId = request.POST["category"]
        category = Category.objects.get(pk=categoryId)
        seller = request.user
        # NEw
        bid = Bids(userBid=request.user, listingBid=0)
        bid.save()
        aucton = AuctionListings.objects.create(title=title, description=description, startingBid=startingBid, imageUrl=imageUrl, seller=seller, category=category, bids=bid)
        aucton.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })

@login_required(login_url='login')
def watchlist_view(request):
    return render(request, "auctions/watchlist.html")

def category_view(request, name):
    category = Category.objects.get(name=name.capitalize())
    listing = AuctionListings.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "categoryName": category.name,
        "auctionListings": listing
    })

def categories_view(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })