# Generated by Django 4.1.5 on 2023-08-15 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_feeds', '0015_alter_scheduledtaskargs_feed_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledtaskargs',
            name='feed_user',
            field=models.CharField(max_length=200),
        ),
    ]
