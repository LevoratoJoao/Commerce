from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListings, Bids, Comments


def index(request):
    products = AuctionListings.objects.all()
    return render(request, "auctions/index.html", {
        'products': products
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

def product(request, product_id):
    product = AuctionListings.objects.get(pk=product_id)
    return render(request, "auctions/product.html", {
        "product": product
    })

def create_view(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["starting_bid"]
        imageUrl = request.POST["image_url"]
        #seller = User.objects.get(pk=id)
        #aucton = AuctionListings.objects.create(title=title, description=description, startingBid=startingBid, imageUrl=imageUrl, seller=seller)
        #aucton.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html")

def watchlist_view(request):
    return render(request, "auctions/watchlist.html")

def categories_view(request):
    return render(request, "auctions/categories.html")