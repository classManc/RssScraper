# Generated by Django 4.1.5 on 2023-08-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_feeds', '0006_feeditem_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledtaskargs',
            name='request_user',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
