from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("shop", views.shop, name = "shop"),
    path("item", views.item, name = "item"),
    path("login", views.login, name = "login"),
    path("register", views.register, name = "register"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name = "add_to_cart"),
    path("add_to_wishlist/", views.add_to_wishlist, name = "add_to_wishlist"),
    path("remove_item", views.remove_from_cart, name = "remove_from_cart"),
    path("remove_from_wishlist", views.remove_from_wishlist, name = "remove_from_wishlist"),

    path("orders", views.orders, name = "orders"),
    path("wishlist", views.wishlist, name = "wishlist"),
    path("logout", views.logout, name = "logout"),
    path("payment", views.payment, name = "payment"),
    path("clear_cart", views.clear_cart, name = "clear_cart"),
    path("add_review/<int:funko_id>/", views.add_review, name="add_review"),

    path("add_all_to_cart", views.add_all_to_cart, name = "add_all_to_cart"),
    path("clear_wishlist", views.clear_wishlist, name = "clear_wishlist"),

]
