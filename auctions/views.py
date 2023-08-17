from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Auctionlistings
from .models import User
from .models import Comments
from .models import Bids
import imghdr
import urllib.request

def index(request):
    auctionlisting=Auctionlistings.objects.all()
    return render(request, "auctions/index.html",{
        "listings":auctionlisting
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createlisting(request):
    if request.method=="POST":
        auctionlisting=Auctionlistings()
        auctionlisting.auction_listing=request.POST["title"]
        auctionlisting.description=request.POST["description"]
        auctionlisting.image_url=request.POST["imageurl"]
        auctionlisting.category=request.POST["Category"]
        auctionlisting.owner=request.user.username
        auctionlisting.inital_bid=request.POST["inital_bid"]
        auctionlisting.save()
        ##################
        bid=Bids.objects.create(Bidder=request.user,Item=auctionlisting,Bid=auctionlisting.inital_bid)
        ###################
        user=request.user
        user.ownership.add(auctionlisting)
        ###################
        return HttpResponseRedirect(reverse("index"))
    return render(request,"auctions/createlistings.html")

def item(request,item):
    alert_msg=None
    sample=request.user
    sample_item=Auctionlistings.objects.get(auction_listing=item)
    if sample_item in sample.ownership.all() :
        code=1
    else :
        code=0
    if request.method=="POST":
        form_id = request.POST.get('form_id')
        print(form_id)
        if form_id=="Submit Comment":
            comment=Comments()
            comment.Commentator=request.user.username
            comment.Comment=request.POST["Comment"]
            comment.item_c=item
            comment.save()
        elif form_id=="watchlist":
            user=request.user
            user.watchlist.add(Auctionlistings.objects.get(auction_listing=item))
            watchlists=user.watchlist.all()
            return render(request,"auctions/watchlist.html",{
         "listings":watchlists
            })
        elif form_id=="Already in watchlist":
            user=request.user
            user.watchlist.remove(Auctionlistings.objects.get(auction_listing=item))
            watchlists=user.watchlist.all()
            return render(request,"auctions/watchlist.html",{
         "listings":watchlists
            })
        elif form_id=="Placebid":
            item=Auctionlistings.objects.get(auction_listing=item)
            bids_for_listing=item.item.all()
            bef_bid=[b.Bid for b in bids_for_listing]
            if int(request.POST["Bid"])> bef_bid[-1] :
                bid=Bids.objects.get(Item=item)
                bid.Bidder=request.user
                bid.Bid=request.POST["Bid"]
                bid.save()
            else :
                alert_msg=" Your Bid is less than Current Bid"
    if Comments.objects.filter(item_c=item):
        comments=Comments.objects.filter(item_c=item)
    else :
        comments=None
    sample=request.user
    sample_item=Auctionlistings.objects.get(auction_listing=item)
    if sample_item in sample.watchlist.all() :
        message="Already in watchlist"
    else :
        message="watchlist"
    listing=Auctionlistings.objects.get(auction_listing=item)
    bids_for_listing=listing.item.all()
    bid=[b.Bid for b in bids_for_listing]
    return render(request,"auctions/item.html",{
        "item":Auctionlistings.objects.get(auction_listing=item),
        "comments":comments,
        "message":message,
        "code":code,
         "price":bid[-1],
         "alert":alert_msg
    })

def watchlist(request):
    user=request.user
    watchlist=user.watchlist.all()
    return render(request,"auctions/watchlist.html",{
         "listings":watchlist,
         "count":watchlist.count()
    })
