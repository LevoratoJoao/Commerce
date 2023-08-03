from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("categories", views.categories_view, name="categories"),
    path("product/<int:product_id>", views.product, name="product"),
    path("create", views.create_view, name="create")
]
