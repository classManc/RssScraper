# Generated by Django 4.1.5 on 2023-09-07 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_resettoken_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resettoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 7, 19, 46, 10, 922977, tzinfo=datetime.timezone.utc)),
        ),
    ]