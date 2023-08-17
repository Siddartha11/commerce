from django.contrib.auth.models import AbstractUser
from django.db import models

class Auctionlistings(models.Model):
    auction_listing=models.CharField(max_length=64)
    description=models.TextField(default='No description availiable')
    image_url=models.TextField( default='No image avaliable')
    category=models.CharField(max_length=64, default='Uncategorized')
    owner=models.CharField(max_length=32,default='Anonymous')
    intial_bid=models.IntegerField(default=0)
    def __str__(self):
        return f"{self. auction_listing}"

class User(AbstractUser):
    ownership=models.ManyToManyField(Auctionlistings,blank=True,related_name="ownership")
    watchlist=models.ManyToManyField(Auctionlistings,blank=True,related_name="watchlist")
    pass

class Bids(models.Model):
    Bidder=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bidder")
    Item = models.ForeignKey(Auctionlistings,on_delete=models.CASCADE,related_name="item")
    Bid=models.IntegerField()
    def __str__(self):
        return f"Current Bid on  {self.Item} is {self.Bid}"


class Comments( models.Model):
    Commentator=models.CharField(max_length=64,default='anonymous')
    Comment=models.TextField()
    item_c=models.CharField(max_length=64,default='anonymous')
    def __str__(self):
        return f"On {self.item_c} : {self.Comment}"