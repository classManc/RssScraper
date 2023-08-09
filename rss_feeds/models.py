from django.db import models
from django.contrib.auth.models import User



#Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Category'

class Feeds(models.Model):
    name = models.CharField(max_length=250)
    url = models.URLField(max_length=250, blank=False)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = 'Feeds'


class FeedItem(models.Model):
    feed = models.ForeignKey(Feeds, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_read = models.BooleanField(default=False)
    # pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ScheduledTaskArgs(models.Model):
    url = models.URLField()
    feed_id = models.IntegerField()

