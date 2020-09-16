from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

now = timezone.now()

class User(AbstractUser):
    watching = models.ManyToManyField('Auction', related_name='watching', blank=True)
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    CATEGORIES = (
        ('NON', '-----'),
        ('MUS', 'Music'),
        ('TEC', 'Technology'),
        ('SPO', 'Sports'),
        ('ART', 'Art'),
        ('FAS', 'Fashion'),
        ('HOM', 'Home'),
        ('OFF', 'Office'),
        ('TRA', 'Transport'),
        ('OTH', 'Other')
    )
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    img_url = models.URLField()
    category = models.CharField(
        max_length=3,
        choices=CATEGORIES
    )
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.title} - £{self.starting_bid})"


class Auction(models.Model):
    listing_auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_auction")
    no_of_bids = models.IntegerField(default=0)
    bidding_open = models.BooleanField(default=True)
    def __str__(self):
        if self.bidding_open:
            status = "open"
        else:
            status = "closed"
        return f"Listing #{self.listing_auction.id} has {self.no_of_bids} bids - bidding {status}"

class Bid(models.Model):
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    bid_auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid_auction")
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"User #{self.bid_user.id} bid £{self.bid_amount:.2f} on auction #{self.bid_auction.id}"


class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    comment_auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment_auction")
    message = models.TextField()
    time_sent = models.DateTimeField()

    def __str__(self):
        return f"{self.comment_user} commented on auction #{self.comment_auction.id} at {self.time_sent}:\n {self.message}"


