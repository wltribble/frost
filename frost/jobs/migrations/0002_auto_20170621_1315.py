# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 17:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='job',
            table='JobOperations',
        ),
    ]
