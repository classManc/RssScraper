# Generated by Django 4.1.5 on 2023-08-15 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rss_feeds', '0009_remove_scheduledtaskargs_request_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feeds',
            name='user',
        ),
        migrations.AddField(
            model_name='feeds',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]