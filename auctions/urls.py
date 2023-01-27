from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing", views.listing, name="listing"),
    path("category/<str:category>", views.view_category, name="category"),
    path("item/<int:id>", views.view_item, name="item"),
    path("bid/<int:id>", views.new_bid, name="bid"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)