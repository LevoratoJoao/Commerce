from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models import Max

class User(AbstractUser, models.Model):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    startingBid = models.FloatField(default=0.0)
    imageUrl = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    active = models.BooleanField(default=True)
    creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    saleDate = models.DateTimeField(null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="seller")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return f"Title: {self.title} Category: {self.category}"

    def getListingBid(self):
        return self.auctionListingBid.aggregate(Max("bid"))['bid__max']

class Bids(models.Model):
    userBid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBid")
    auctionListing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="auctionListingBid")
    bid = models.FloatField(default=0)
    creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Comments(models.Model):
    userComment = models.ForeignKey(User, on_delete=models.CASCADE)
    listingComment = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)