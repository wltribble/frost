# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 19:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('embossers', '0027_auto_20170609_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='process_outline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processes.Process'),
        ),
    ]