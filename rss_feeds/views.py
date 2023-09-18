from django.shortcuts import render
from django.http import HttpResponse
from .serializers import CategorySerializer, FeedsSerializer,FeedItemSerializer
from .models import Feeds, FeedItem, ScheduledTaskArgs
from rest_framework.views import APIView
from rest_framework.response import Response
from rss_feeds.tasks import scrape_site, my_scheduled_task
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.
### View for Listing and Creating feeds



class ListFeeds(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Page number',
                required=False,
            ),
            openapi.Parameter(
                name='page_size',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Number of items per page',
                required=False,
            ),
        ],
    )

    def get(self, request):
        search_term = request.query_params.get('search', '')
        feeds = Feeds.objects.filter(user=request.user)
        
        if search_term:
            feeds = feeds.filter(name__icontains=search_term) | feeds.filter(url__icontains=search_term)

        ordering = request.query_params.get('ordering', 'name')  # Default to ordering by name
        feeds = feeds.order_by(ordering)
        
        paginator = self.pagination_class()
        paginator.page_size = 1
        page_size = request.query_params.get('page_size', paginator.page_size)  # Get the per_page value or use the default
        paginator.page_size = page_size  # Set the page size to the per_page value
        paginated_feeds = paginator.paginate_queryset(feeds, request)
        serializer = FeedsSerializer(paginated_feeds, many=True)

        # Add pagination information to the response headers
        response = paginator.get_paginated_response(serializer.data)
        response['X-Total-Count'] = feeds.count()  # Total count of items
        response['X-Total-Pages'] = paginator.page.paginator.num_pages  # Total number of pages

        return response

    
    @swagger_auto_schema(
        request_body=FeedsSerializer,
        responses={201: FeedsSerializer},
    )
    def post(self,request):
        serializer = FeedsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            if Feeds.objects.filter(name=serializer.validated_data['name'], url=serializer.validated_data['url'], user=serializer.validated_data['user']).exists():
                return Response({'error':'Data already exists for user'})
            serializer.save()

            new_feed = Feeds.objects.filter(user=request.user).last() # get the last feed created by the user
            scrape_site.delay(serializer.validated_data['url'], new_feed.id, request.user.id) 
            ScheduledTaskArgs.objects.create(url=serializer.validated_data['url'], feed_id=new_feed.id, feed_user=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### View for Retrieving and Deleting feeds  
class RetrieveFeeds(APIView):
    permission_classes= [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Feeds.objects.get(pk=pk)
        except Feeds.DoesNotExist:
            return HttpResponse(status=404)
    
    def get(self, request, pk):
        feed = self.get_object(pk=pk)
        if request.user == feed.user:
            serializer = FeedsSerializer(feed)
            return Response(serializer.data)
        return Response({'error_message':'NotFound'}, status=404)


    def delete (self, request, pk):
        feed = self.get_object(pk=pk)
        if request.user == feed.user:
            feed.delete()
        return Response({'error_message':'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    

##### view for getting feeditems belonging to one feed
class RetrieveFeedItem(APIView):
    permission_classes= [IsAuthenticated,]
    filter_backends = [SearchFilter,OrderingFilter]
    pagination_class = PageNumberPagination

    def get_object(self,pk):
        try:
            return Feeds.objects.get(pk=pk)
        except Feeds.DoesNotExist:
            return HttpResponse(status=404)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Page number',
                required=False,
            ),
            openapi.Parameter(
                name='page_size',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Number of items per page',
                required=False,
            ),
        ],
    )
    
    def get(self, request, pk):
        feed = self.get_object(pk=pk)
        if  request.user == feed.user:
            search_term = request.query_params.get('search', '')
            feed_items = feed.feeditem_set.all()
            if search_term:
                feed_items = feed_items.filter(title__icontains=search_term) | feed_items.filter(description__icontains=search_term)
            for item in feed_items:
                if item.is_read == True:
                    pass
                else:
                    item.is_read = True
                    item.save()
            ordering = request.query_params.get('ordering', 'title')  # Default to ordering by title
            feed_items = feed_items.order_by(ordering)
            paginator = self.pagination_class()
            paginator.page_size = 1
            page_size = request.query_params.get('page_size', paginator.page_size)  # Get the per_page value or use the default
            paginator.page_size = page_size  # Set the page size to the per_page value
            paginated_feed_items = paginator.paginate_queryset(feed_items, request)
            serializer = FeedItemSerializer(paginated_feed_items, many=True)  # Use paginated_feeds here
            return paginator.get_paginated_response(serializer.data)
        return Response({'error_message':'NotFound'}, status=404)
        
        
    
#  View to list all feed items globally
class GenericFeedItemList(APIView):
    permission_classes= [IsAuthenticated,]
    filter_backends = [SearchFilter,OrderingFilter]
    pagination_class = PageNumberPagination


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Page number',
                required=False,
            ),
            openapi.Parameter(
                name='page_size',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Number of items per page',
                required=False,
            ),
        ],
        responses={200: openapi.Response(description='Successful response', schema=FeedItemSerializer)},
    )
    def get(self, request):
        search_term = request.query_params.get('search', '')
        feed_items = FeedItem.objects.filter(feed__user=request.user)
        if search_term:
            feed_items = feed_items.filter(title__icontains=search_term) | feed_items.filter(description__icontains=search_term)
        for item in feed_items:
            if item.is_read == True:
                pass
            else:
                item.is_read = True
                item.save()
        ordering = request.query_params.get('ordering', 'title')  # Default to ordering by title
        feed_items = feed_items.order_by(ordering)


        paginator = self.pagination_class()
        paginator.page_size = 1
        page_size = request.query_params.get('page_size', paginator.page_size)  # Get the per_page value or use the default
        paginator.page_size = page_size  # Set the page size to the per_page value
        paginated_feed_items = paginator.paginate_queryset(feed_items, request)
        serializer = FeedItemSerializer(paginated_feed_items, many=True)

        # Add pagination information to the response headers
        response = paginator.get_paginated_response(serializer.data)
        response['X-Total-Count'] = feed_items.count()  # Total count of items
        response['X-Total-Pages'] = paginator.page.paginator.num_pages  # Total number of pages

        return response