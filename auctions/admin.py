from django.contrib import admin
from .models import User, Listing, Comments, Bids

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comments)
admin.site.register(Bids)
