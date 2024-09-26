from django.contrib import admin

from restaurants.models import Restaurant, Review

admin.site.register(Restaurant)
admin.site.register(Review)
