# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embossers', '0032_auto_20170609_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='process_outline',
            field=models.IntegerField(choices=[(0, 'New Process Template'), (1, 'Some Process'), (2, 'None'), (3, 'another process')], default='None'),
        ),
    ]
