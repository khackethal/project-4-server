from django.contrib import admin
from .models import Trip, Comment, UserTripList

admin.site.register(Trip)
admin.site.register(Comment)
admin.site.register(UserTripList)