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
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    img = models.ImageField(upload_to="images", default=None)
    
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now, blank=True)
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now, blank=True)