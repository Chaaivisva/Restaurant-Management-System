from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, Pending, Profile, RestaurantCategory, Order

admin.site.register(Restaurant)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(Pending)
admin.site.register(Profile)
admin.site.register(RestaurantCategory)
admin.site.register(Order)