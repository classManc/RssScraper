# Generated by Django 4.1.5 on 2023-08-02 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rss_feeds', '0003_feeditem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feeds',
            name='categories',
        ),
        migrations.AddField(
            model_name='feeds',
            name='categories',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rss_feeds.category'),
            preserve_default=False,
        ),
    ]
