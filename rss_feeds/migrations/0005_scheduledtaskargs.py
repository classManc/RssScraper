# Generated by Django 4.1.5 on 2023-08-03 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_feeds', '0004_remove_feeds_categories_feeds_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTaskArgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('feed_id', models.IntegerField()),
            ],
        ),
    ]
