# Generated by Django 3.0.4 on 2020-06-22 15:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20200622_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jhudata',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 6, 22, 15, 20, 1, 496194, tzinfo=utc)),
        ),
    ]