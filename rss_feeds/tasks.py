from celery import shared_task
import bs4
import requests
from .models import FeedItem, ScheduledTaskArgs
from .serializers import FeedItemSerializer

@shared_task
def scrape_site(url, id):
    site_data = requests.get(url)
    soup = bs4.BeautifulSoup(site_data.text, 'xml')
    parsed_site_title = soup.select('title')[0].text
    parsed_site_description = soup.select('description')[0].text
    if FeedItem.objects.filter(title=parsed_site_title, description=parsed_site_description).exists():
        return None
    FeedItem.objects.create(title=parsed_site_title, description=parsed_site_description, feed_id=id)

@shared_task
def my_scheduled_task():
    # Retrieve the arguments from the database
       all_task_args = ScheduledTaskArgs.objects.all()
       for task_args in all_task_args:
           url = task_args.url
           feed_id = task_args.feed_id
           return scrape_site.delay(url, feed_id)