# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 17:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OutlineField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OUTLINE_field_name', models.CharField(max_length=100)),
                ('OUTLINE_field_text', models.CharField(blank=True, max_length=200)),
                ('OUTLINE_name_is_operator_editable', models.BooleanField(default=True)),
                ('OUTLINE_text_is_operator_editable', models.BooleanField(default=True)),
                ('OUTLINE_required_for_full_submission', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(default='New Process Template', max_length=100, unique=True)),
                ('process_date_created', models.DateTimeField(auto_now_add=True, verbose_name='process date created')),
                ('job_type', models.CharField(default='embosser', max_length=100, verbose_name='job type')),
            ],
            options={
                'verbose_name_plural': 'processes',
            },
        ),
        migrations.AddField(
            model_name='outlinefield',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processes.Process'),
        ),
    ]
