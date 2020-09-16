from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from datetime import datetime

from .models import User, Listing, Bid, Auction, Comment
from . import forms

def index(request):
    try:
        watch_count = User.objects.get(pk=request.user.id).watching.count()
    except User.DoesNotExist:
        watch_count = 0
    return render(request, "auctions/index.html", {
        "open_auctions": Listing.objects.filter(listing_auction__bidding_open=True),
        "categories": Listing.CATEGORIES[1:],
        "watch_count": watch_count
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
            return redirect("index")
        else:
            messages.error(request, 'Invalid username and/or password.')
            return redirect("login")
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, 'Passwords must match.')
            return redirect("register")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(request, f"'{username}' is already taken - try another username.")
            return redirect("register")
        login(request, user)
        messages.success(request, 'Sign-up successful - welcome aboard!')
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = forms.CreateForm(request.POST)
        if form.is_valid():
            # unable to save form until user_id is added
            new_listing = form.save(commit=False)
            new_listing.listing_user = User.objects.get(pk=int(request.user.id))
            open_auction = Auction(listing_auction=new_listing)
            new_listing.save()
            open_auction.save()
            messages.success(request, 'Listing added - good luck!')
            return redirect("listing", listing_path=new_listing.id)
        else:
            messages.error(request, 'Invalid form input - please try again.')
            return redirect("index")

    else:
        return render(request, "auctions/create.html", {
            "create_form": forms.CreateForm,
            "username": request.user.username,
            "categories": Listing.CATEGORIES[1:],
            "watch_count": User.objects.get(pk=request.user.id).watching.count()
        })


@login_required(login_url="login")
def listing(request, listing_path):
    listing = Listing.objects.get(pk=int(listing_path))
    user = User.objects.get(pk=int(request.user.id))
    auction = Auction.objects.get(listing_auction=listing)
    if request.method == "POST":
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data["message"]
            Comment.objects.create(
                comment_user=user, 
                comment_auction=auction, 
                message=comment, 
                time_sent=datetime.now())
            messages.success(request, 'Thanks for the comment!')
            return redirect("listing", listing_path=listing_path)
        else:
            messages.error(request, 'Invalid form input - please try again.')
            return redirect("index")
    else:
        comments = auction.comment_auction.all().order_by('-time_sent')
        watching = auction.watching.filter(pk=int(user.id))
        bidding = auction.bid_auction.filter(bid_user=int(user.id)).first()
        winning = auction.bid_auction.order_by('-bid_amount').first()
        
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "auction": auction,
            "watching": watching,
            "bidding": bidding,
            "winning": winning,
            "comments": comments,
            "comment_form": forms.CommentForm,
            "categories": Listing.CATEGORIES[1:],
            "watch_count": User.objects.get(pk=request.user.id).watching.count()

        })


def category(request, cat_path):
    try:
        watch_count = User.objects.get(pk=request.user.id).watching.count()
    except User.DoesNotExist:
        watch_count = 0
    return render(request, "auctions/category.html", {
        "category": Listing.objects.filter(category=cat_path).filter(listing_auction__bidding_open=True),
        "categories": Listing.CATEGORIES[1:],
        "watch_count": watch_count
    })


def profile(request, user_path):
    try:
        watch_count = User.objects.get(pk=request.user.id).watching.count()
    except User.DoesNotExist:
        watch_count = 0
    profile_user = User.objects.get(username=user_path)
    profile_listings = Listing.objects.filter(listing_user=profile_user.id)
    return render(request,"auctions/profile.html", {
        "profile_user": profile_user,
        "open_auctions": profile_listings.filter(listing_auction__bidding_open=True),
        "closed_auctions": profile_listings.filter(listing_auction__bidding_open=False),
        "categories": Listing.CATEGORIES[1:],
        "watch_count": watch_count
    })


@login_required(login_url="login")
def watching(request):
    user = User.objects.get(pk=int(request.user.id))
    if request.method == "POST":
        form = int(request.POST["auction"])
        auction = Auction.objects.get(listing_auction=form)
        watching = auction.watching.filter(pk=int(user.id))
        if watching:
            user.watching.remove(auction)
        else:
            user.watching.add(auction)
        return redirect("listing", listing_path=form)
    else:
        return render(request, "auctions/watchlist.html", {
        "watchlist": Listing.objects.filter(listing_auction__watching=user.id),
        "categories": Listing.CATEGORIES[1:],
        "watch_count": User.objects.get(pk=request.user.id).watching.count()
    })


@login_required(login_url="login")
def close(request, listing_path):
    if request.method == "POST":
        close_request = request.POST['close']
        if close_request == "Close":
            closing = Auction.objects.get(listing_auction=listing_path)
            winner = closing.bid_auction.order_by('-bid_amount').first()
            closing.bidding_open = False
            closing.save()
            if winner == None:
                messages.info(request, f"Bidding for {closing.listing_auction.title} - sorry that nobody bid high enough this time.")
            else:
                messages.success(request, f"Going... Going... Gone! Sold '{closing.listing_auction.title}' for £{winner.bid_amount:.2f}.")
            return redirect("index")


@login_required(login_url="login")
def bid(request, listing_path):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(listing_path))
        auction = listing.listing_auction.get()
        user = User.objects.get(pk=int(request.user.id))
        if auction.bidding_open:
            new_bid = float(request.POST['bid_amount'])
            current_bids = Bid.objects.filter(bid_auction=auction)
            if new_bid < listing.starting_bid or current_bids.filter(bid_amount__gte=new_bid):
                user.watching.add(auction)
                messages.error(request, f"Sorry, your bid of £{new_bid:.2f}, wasn\'t quite enough - try again.")
                return redirect("listing", listing_path=listing_path)
            else:
                user = User.objects.get(pk=int(request.user.id))
                place_bid = Bid.objects.create(bid_user=user, bid_auction=auction, bid_amount=new_bid)
                auction.no_of_bids += 1
                auction.save()
                user.watching.add(auction)
                messages.success(request, f"You're winning! Bid of £{new_bid:.2f} placed for '{listing.title}'.")
                return redirect("index")
        else:
            messages.error(request, f"Sorry, you missed the boat - bidding on this item is closed.")
            return redirect("listing", listing_path=listing_path)
    else:
        return redirect("listing", listing_path=listing_path)
