# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0002_auto_20170609_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlinefield',
            name='OUTLINE_field_name',
            field=models.CharField(max_length=100),
        ),
    ]
