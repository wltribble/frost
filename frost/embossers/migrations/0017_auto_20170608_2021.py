# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 20:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embossers', '0016_auto_20170608_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='full_editable',
        ),
        migrations.RemoveField(
            model_name='field',
            name='only_value_editable',
        ),
    ]