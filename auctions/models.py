from datetime import datetime
from email.policy import default
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = [
        ("NONE", "None"),
        ("ELECTRONICS", "Electronics"),
        ("ART", "Art"),
        ("CLOTHING", "Clothing"),
        ("TOYS", "Toys"),
        ("BOOKS, MOVIES, MUSIC", "Books, Movies, Music"),
        ("HEALTH, BEAUTY", "Health, Beauty"),
        ("PET SUPPLIES", "Pet Supplies")
        
    ]
    
    title = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORIES, default="NONE", max_length=25)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now, blank=True)
    date_end = models.DateTimeField(default=datetime.now) # TODO: hacky fix
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    img = models.ImageField(upload_to="images", default=None, blank=True) 
    
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    max_bid = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now, blank=True)
    number_bids = models.IntegerField(default=0)

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now, blank=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Bought(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)


