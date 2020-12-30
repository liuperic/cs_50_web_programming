from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_owner")
    opening_bid = models.DecimalField(max_digits=19, decimal_places=2)
    bid = models.ForeignKey("Bid", on_delete=models.CASCADE, blank=True, null=True)
    bids = models.ManyToManyField("Bid", related_name="all_bids", blank=True)
    ongoing = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Bid(models.Model):
    bid = models.DecimalField(max_digits=19, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bidder")
    total_bids = models.IntegerField()
    time = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.bid}"

class Comment(models.Model):
    comment = models.TextField()
    time = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_commenter")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="related_auction")




