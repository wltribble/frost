# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embossers', '0042_remove_job_submit_button_disabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='disable_submit_button',
            field=models.BooleanField(default=False),
        ),
    ]