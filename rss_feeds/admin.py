from django.contrib import admin
from.models import Category, Feeds,FeedItem,ScheduledTaskArgs

# Register your models here.
admin.site.register(Category)
admin.site.register(Feeds)
admin.site.register(FeedItem)
admin.site.register(ScheduledTaskArgs)