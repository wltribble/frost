# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embossers', '0046_auto_20170612_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='assembly_number',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='job',
            name='job_number',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='job',
            name='operation_number',
            field=models.CharField(default='', max_length=100),
        ),
    ]
