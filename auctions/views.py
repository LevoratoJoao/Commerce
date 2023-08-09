import datetime
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
        'listings': listings,
        'message': "All Listings"
    })

def displayListings(request, option):
    if option == "active":
        listings, message = AuctionListings.objects.filter(active=True), "Active Listings"
    else:
        listings, message = AuctionListings.objects.filter(active=False), "Inactive Listings"
    return render(request, "auctions/index.html", {
        'listings': listings,
        'message': message
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
    bid = Bids.objects.filter(auctionListing=listing).last()
    comments = Comments.objects.filter(listingComment=listing)
    isWatching = request.user in listing.watchlist.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": bid,
        "comments": comments,
        "isWatching": isWatching
    })

def addBid(request, id):
    if request.method == "POST":
        listing = AuctionListings.objects.get(pk=id)
        listingBid = float(request.POST["listingBid"])
        listingMaxBid = listing.auctionListingBid.aggregate(Max("bid"))['bid__max']
        if listingBid <= listing.startingBid:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Error: Your bid has to be greater than the starting bid",
                "bid": Bids.objects.filter(auctionListing=listing).last()
            })
        elif listingBid <= listingMaxBid:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Error: Your bid has to be greater than the current bid",
                "bid": Bids.objects.filter(auctionListing=listing).last()
            })
        bid = Bids.objects.create(userBid=request.user, auctionListing=listing, bid=listingBid)
        bid.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))

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
        listing = AuctionListings.objects.create(title=title, description=description, startingBid=startingBid, imageUrl=imageUrl, seller=seller, category=category)
        listing.save()
        bid = Bids.objects.create(userBid=seller, auctionListing=listing, bid=0)
        bid.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })

@login_required(login_url='login')
def watchlist_view(request):
    watchlist = AuctionListings.objects.filter(watchlist=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

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

@login_required(login_url='login')
def addComment(request, id):
    if request.method == "POST":
        listing = AuctionListings.objects.get(pk=id)
        commentContent = request.POST["comment"]
        comment = Comments.objects.create(userComment=request.user, listingComment=listing, comment=commentContent)
        comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

@login_required(login_url='login')
def deleteComment(request, listingId, commentId):
    comment = Comments.objects.get(pk=commentId)
    comment.delete()
    return HttpResponseRedirect(reverse("listing", args=(listingId,)))

@login_required(login_url='login')
def addWatchlist(request, id):
    listing = AuctionListings.objects.get(pk=id)
    listing.watchlist.add(request.user)
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

@login_required(login_url='login')
def removeWatchlist(request, id):
    listing = AuctionListings.objects.get(pk=id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

@login_required(login_url='login')
def closeListing(request, id):
    listing = AuctionListings.objects.get(pk=id)
    listing.active = False
    listing.buyer = request.user
    listing.saleDate = datetime.datetime.now().date()
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))