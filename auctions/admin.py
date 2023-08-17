from django.contrib import admin
from .models import Auctionlistings,User,Bids,Comments

# Register your models here.


admin.site.register(Auctionlistings)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comments)