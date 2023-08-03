from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, models.Model):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    startingBid = models.FloatField(default=0)
    imageUrl = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    active = models.BooleanField(default=True)
    creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    saleDate = models.DateTimeField(null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="seller")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass