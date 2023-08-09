from django.shortcuts import render
from django.http import HttpResponse
from .serializers import CategorySerializer, FeedsSerializer,FeedItemSerializer
from .models import Feeds,FeedItem, ScheduledTaskArgs
from rest_framework.views import APIView
from rest_framework.response import Response
from rss_feeds.tasks import scrape_site, my_scheduled_task
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
### View for Listing and Creating feeds
class ListFeeds(APIView):
    authentication_classes = [BasicAuthentication,]
    permission_classes= [IsAuthenticated,]

    def get(self, request):
        feeds = Feeds.objects.filter(user=request.user)
        serializer = FeedsSerializer(feeds, many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer = FeedsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_feed = Feeds.objects.filter(user=request.user).last()
            scrape_site.delay(serializer.validated_data['url'], new_feed.id) 
            ScheduledTaskArgs.objects.create(url=serializer.validated_data['url'], feed_id=new_feed.id)
            # my_scheduled_task.delay()
            return Response(serializer.data)
        return Response(serializer.error)

### View for Retrieving and Deleting feeds  
class RetrieveFeeds(APIView):
    authentication_classes = [BasicAuthentication,]
    permission_classes= [IsAuthenticated,]

    def get_object(self,pk):
        try:
            return Feeds.objects.get(pk=pk)
        except Feeds.DoesNotExist:
            return HttpResponse(status=404)
    
    def get(self, request, pk):
        feed = self.get_object(pk=pk)
        if  request.user in  feed.user.all():
            serializer = FeedsSerializer(feed)
            return Response(serializer.data)
        return Response({'error_message':'NotFound'}, status=404)


    def delete (self, request, pk):
        feed = self.get_object(pk=pk)
        if  request.user in feed.user.all():
            feed.delete()
        return Response({'error_message':'Deleted Successfully'}, status=404)
    
    

##### view for getting feeditem belonging to one feed
class RetrieveFeedItem(APIView):
    authentication_classes = [BasicAuthentication,]
    permission_classes= [IsAuthenticated,]

    def get_object(self,pk):
        try:
            return Feeds.objects.get(pk=pk)
        except Feeds.DoesNotExist:
            return HttpResponse(status=404)
    
    def get(self, request, pk):
        if len(request.query_params) == 0:
            feed = self.get_object(pk=pk)
            if  request.user in feed.user.all():
                feed_items = feed.feeditem_set.all()
                for item in feed_items:
                    if item.is_read == True:
                        pass
                    else:
                        item.is_read = True
                        item.save()
                serializer = FeedItemSerializer(feed_items, many=True)
                return Response(serializer.data)
            return Response({'error_message':'NotFound'}, status=404)
        
        elif request.query_params['is_read'] == "True":
            feed = self.get_object(pk=pk)
            if  request.user in feed.user.all():
                feed_items = feed.feeditem_set.filter(is_read=True)
                serializer = FeedItemSerializer(feed_items, many=True)
                return Response(serializer.data)
            return Response({'error_message':'NotFound'}, status=404)
        
        else:          
            feed = self.get_object(pk=pk)
            if  request.user in feed.user.all():
                feed_items = feed.feeditem_set.filter(is_read=False)
                for item in feed_items:
                        item.is_read = True
                        item.save()
                serializer = FeedItemSerializer(feed_items, many=True)
                return Response(serializer.data)
            return Response({'error_message':'NotFound'}, status=404)
    
        
    
#  View to list all feed items globally
class GenericFeedItemList(APIView):
    authentication_classes = [BasicAuthentication,]
    permission_classes= [IsAuthenticated,]

    def get(self, request):
        items ={}
        feeds = Feeds.objects.filter(user=request.user)
        if len(request.query_params) == 0:
            for feed in feeds:
                serializer = FeedItemSerializer(feed.feeditem_set.all(), many=True)
                items[feed.name]= serializer.data
            return Response(items)
        
        elif request.query_params['is_read'] == "True":
            for feed in feeds:
                serializer = FeedItemSerializer(feed.feeditem_set.filter(is_read=True), many=True)
                items[feed.name]= serializer.data
            return Response(items)
        else:
            for feed in feeds:
                serializer = FeedItemSerializer(feed.feeditem_set.filter(is_read=False), many=True)
                items[feed.name]= serializer.data
            return Response(items)

    
    
