from django.urls import path
from .views import ListFeeds, RetrieveFeeds, RetrieveFeedItem,GenericFeedItemList

urlpatterns = [
    path('', ListFeeds.as_view(), name='listfeeds'),
    path('feeditems/', GenericFeedItemList.as_view(), name='genriclistfeeditem'),
    path('<int:pk>/', RetrieveFeeds.as_view(), name='retrievefeeds' ),
    path('<int:pk>/feeditem/', RetrieveFeedItem.as_view(), name='retrieveitemfeeds' )
]