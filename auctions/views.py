from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Comments, Bids

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all
    })


class NewCommentForm(forms.Form):
    # form to write a new comment
    content = forms.CharField(max_length=500, required=False,
                            widget= forms.Textarea
                           (attrs={
                               'class': 'comment',
                               'name': 'Comment',
                               'placeholder':'Enter your comment here',
                               'required': 'True'
                            }))


class NewBidForm(forms.Form):
    # form to give a new bid
    bid = forms.DecimalField(max_digits=10, decimal_places=2, required=False,
                                widget= forms.NumberInput #TODO: test
                           (attrs={
                               'class': 'bid',
                               'name': 'Bid',
                               'placeholder':'',
                               'required': 'True'
                            }))

def view_item(request, id):
    if request.method == "POST":
        ''' post a new comment '''

        content = request.POST["content"]
        # get current user's id
        user = request.user
        product = Listing.objects.get(id=id) # TODO: hacky fix 

        # save the comment in db
        comment = Comments(user=user, product=product, comment=content)
        comment.save()
        
        # reload the item page of the specific item
        return HttpResponseRedirect(str(id))
        
    else:
        return render(request, "auctions/item.html", {
            "listing": Listing.objects.get(id=id),
            "comments": Comments.objects.filter(product_id=id),
            "form_comment": NewCommentForm(request.POST),
            "bids": Bids.objects.get(product_id=id),
            "form_bid": NewBidForm(request.POST)
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

class NewListingForm(forms.Form):
    # form to add a new product to sell

    title = forms.CharField(label="Title", required=True,
                            widget= forms.TextInput
                           (attrs={
                               'class': 'title',
                               'name': 'Title',
                               'placeholder':'',
                               'required': 'True'
                            }))
    category = forms.ChoiceField(required=False, choices=Listing.category.field.choices)
    price = forms.DecimalField(label="Starting Price", max_digits=10, decimal_places=2, required=True,
                                widget= forms.NumberInput #TODO: test
                           (attrs={
                               'class': 'price',
                               'name': 'Price',
                               'placeholder':'',
                               'required': 'True'
                            }))
    end = forms.DateTimeField(label="End of Auction", widget=DateTimePickerInput(
                options={
                    "format": "MM/DD/YYYY HH/mm",

                    # TODO: the following throws error "inputElement.dataset is undefined"
                    #"autoclose": True 
                }
            )
        )
                           
    image = forms.ImageField(required=False)
    description = forms.CharField(max_length=500, required=False,
                            widget= forms.Textarea
                           (attrs={
                               'class': 'despcription',
                               'name': 'Description',
                               'placeholder':'',
                               'required': 'True',
                            }))

    # clean_*variable_name* overrides the clean function that is called with .is_valid()                      
    def clean_end(self):
        '''check if end is valid -> date has to be in the future'''

        data = self.cleaned_data["end"]

        # fix error: Can't compare naive and aware datetime.now()
        # sol: datetime.now() ist not timezone aware 
        '''import pytz
        utc = pytz.UTC 

        data = utc.localize(data.replace(tzinfo=utc)) # data posted in form
        now = utc.localize(datetime.datetime.now().replace(tzinfo=utc)) # now'''
        from django.utils import timezone
        now = timezone.now()

        # check if date is not in the past
        if data < now:
            raise ValidationError(_("Invalid date - end of auction in the past!"))
        return data


def listing(request):
    if request.method == "POST":
        # save the new product in db
        title = request.POST["title"]
        category = request.POST["category"]
        price = request.POST["price"]
        end = request.POST["end"]
        image = request.FILES["image"]
        description = request.POST["description"]
        user = request.user

        # check if form is valid, especially if date is not in past
        form = NewListingForm(request.POST)
        if form.is_valid():
            listing = Listing(title=title, category=category, price=price, date_end=end, img=image, description=description, user=user)
            listing.save()

            # save a dummy bid to initiate the bidding process
            #id = listing.id  # TODO: how to get the new id of the saved listing
            bid = Bids(user=user, product=listing, max_bid=0, number_bids=0)
            bid.save()

            # redirect to index page 
            return HttpResponseRedirect("/")
        else:
            # return to form and show error messages
            return render(request, "auctions/listing.html", {
            "form": form
        })
    
    else: 
        return render(request, "auctions/listing.html", {
            "form": NewListingForm(request.POST, request.FILES)
        })

def categories(request):
    # show all categories 

    # fix to get only the second values in CATEGORIES
    categories = [cat[1] for cat in Listing.CATEGORIES]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def view_category(request, category):
    # only show listings of one category
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category.upper())
    })

def watchlist(request):
    return render(request, "auctions/index.html")
