from django.contrib import admin

from .models import User, Listing, Auction, Bid, Comment

# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "bidding_open")


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watching",)

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)