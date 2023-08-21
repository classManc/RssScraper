# Generated by Django 4.1.5 on 2023-08-15 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_feeds', '0010_remove_feeds_user_feeds_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feeds',
            name='categories',
        ),
        migrations.AddField(
            model_name='feeds',
            name='categories',
            field=models.ManyToManyField(to='rss_feeds.category'),
        ),
    ]
