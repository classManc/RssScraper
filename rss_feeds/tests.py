
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Feeds,FeedItem,Category
from .serializers import FeedsSerializer,FeedItemSerializer
from django.contrib.auth.models import User



class NoteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.category = Category.objects.create(name="Sport")
        self.newcat = Category.objects.first()
        self.feed = Feeds.objects.create(
            name="feedburner", url="https://feeds.feedburner.com/tweakers/mixed", 
            user=self.user
        )
        self.feed.categories.add(self.newcat)

        self.valid_payload = {
            "name":"life",
            "url": "https://feeds.feedburner.com/tweakers/mixed",
            "categories": [self.newcat.id]
        }
        self.invalid_payload =  {
            "name": "",
            "url": "",
            "categories": []
        }
    def test_create_valid_feed(self):
        response = self.client.post(
            reverse("listfeeds"), data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_create_invalid_feed(self):
        response = self.client.post(
            reverse("listfeeds"), data=self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_all_feeds(self):
        response = self.client.get(reverse("listfeeds"))
        feeds = response.data.get("results") # extract just the list of notes
        serializer = FeedsSerializer(Feeds.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(feeds, serializer.data)
    
    def test_get_single_feed(self):
        response = self.client.get(
            reverse("retrievefeeds", kwargs={"pk": self.feed.id})
        )
        feed = Feeds.objects.get(pk=self.feed.id)
        serializer = FeedsSerializer(feed)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_feed(self):
        response = self.client.delete(
            reverse("retrievefeeds", kwargs={"pk": self.feed.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    


