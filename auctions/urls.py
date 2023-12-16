from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<str:option>", views.displayListings, name="displayListings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("category/<str:name>", views.category_view, name="category"),
    path("categories", views.categories_view, name="categories"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/addComment", views.addComment, name="addComment"),
    path("listing/<int:id>/bid", views.addBid, name="bid"),
    path("listing/<int:id>/addWatchlist", views.addWatchlist, name="addWatchlist"),
    path("listing/<int:id>/removeWatchlist", views.removeWatchlist, name="removeWatchlist"),
    path("listing/<int:id>/closeListing", views.closeListing, name="closeListing"),
    path("listing/<int:listingId>/deleteComment/<int:commentId>", views.deleteComment, name="deleteComment")
]
