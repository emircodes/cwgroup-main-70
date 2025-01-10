from django.contrib import admin
from .models import User, Hobby, FriendRequest, Notification

# Register your models here.

admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(FriendRequest)
admin.site.register(Notification)
