from celery import shared_task
import bs4
import requests
from .models import FeedItem, ScheduledTaskArgs
from .serializers import FeedItemSerializer

@shared_task
def scrape_site(url, id, user):
    site_data = requests.get(url)
    soup = bs4.BeautifulSoup(site_data.text, 'xml')
    
    title_elements = soup.select('title')
    description_elements = soup.select('description')
    
    num_elements = min(len(title_elements), len(description_elements))
    
    for i in range(num_elements):
        parsed_site_title = title_elements[i].text
        parsed_site_description = description_elements[i].text
        if not FeedItem.objects.filter(title=parsed_site_title, description=parsed_site_description, feed__user=user).exists():
            FeedItem.objects.create(title=parsed_site_title, description=parsed_site_description, feed_id=id)

@shared_task
def my_scheduled_task():
    # Retrieve the arguments from the database
       all_task_args = ScheduledTaskArgs.objects.all()
       for task_args in all_task_args:
           url = task_args.url
           feed_id = task_args.feed_id
           feed_user = task_args.feed_user
           return scrape_site.delay(url, feed_id, feed_user)