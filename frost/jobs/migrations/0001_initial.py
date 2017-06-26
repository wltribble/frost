# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 17:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('field_text', models.CharField(blank=True, max_length=200)),
                ('field_has_been_set', models.BooleanField(default=False)),
                ('editing_mode', models.BooleanField(default=False)),
                ('name_is_operator_editable', models.BooleanField(default=True)),
                ('text_is_operator_editable', models.BooleanField(default=True)),
                ('required_for_full_submission', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(default='New Job', max_length=100, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last updated')),
                ('date_submitted', models.DateTimeField(blank=True, null=True)),
                ('process_outline', models.CharField(default='None', max_length=100, verbose_name='Process Template')),
                ('has_process_outline_been_modified_for_this_operation', models.BooleanField(default=False, verbose_name='Edited Template')),
                ('has_job_name_been_set', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('disable_submit_button', models.BooleanField(default=False)),
                ('job_number', models.CharField(blank=True, max_length=100)),
                ('assembly_number', models.CharField(blank=True, max_length=100)),
                ('operation_number', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='field',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Job'),
        ),
    ]