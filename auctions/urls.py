from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("watching", views.watching, name="watching"),
    path("listing/<str:listing_path>", views.listing, name="listing"),
    path("category/<str:cat_path>", views.category, name="category"),
    path("bid/<str:listing_path>", views.bid, name="bid"),
    path("close/<str:listing_path>", views.close, name="close"),
    path("profile/<str:user_path>", views.profile, name="profile")
]
