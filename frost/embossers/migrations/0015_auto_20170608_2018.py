# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 20:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('embossers', '0014_auto_20170608_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 8, 20, 18, 16, 740975, tzinfo=utc), verbose_name='last updated'),
        ),
    ]