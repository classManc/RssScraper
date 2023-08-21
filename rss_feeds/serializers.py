from rest_framework import serializers
from .models import Category, Feeds, FeedItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FeedsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Feeds
        fields = ('name', 'url', 'categories', 'date_created', 'user')

class FeedItemSerializer(serializers.ModelSerializer):
    is_read = serializers.ReadOnlyField()
    class Meta:
        model = FeedItem
        fields = '__all__'
