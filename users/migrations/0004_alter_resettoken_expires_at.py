# Generated by Django 4.1.5 on 2023-09-04 21:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_resettoken_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resettoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 4, 21, 34, 52, 657766, tzinfo=datetime.timezone.utc)),
        ),
    ]
