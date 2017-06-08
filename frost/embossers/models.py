import datetime

from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Create your models here.
class Job(models.Model):
    job_id = models.CharField(max_length=20)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    last_update = models.DateTimeField('last updated', default=timezone.now())
    date_due = models.DateTimeField('date due')

    def __str__(self):
        return self.job_id

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now
    was_created_recently.admin_order_field = 'date_created'
    was_created_recently.boolean = True
    was_created_recently.short_description = 'Created recently?'



class FieldManager(models.Manager):
    def create_field(self, job, field_name, field_text):
        field = self.create(job=job, field_name=field_name, field_text=field_text)
        return field


class Field(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    field_text = models.CharField(max_length=200, blank=True)
    field_has_been_set = models.BooleanField(default=False)
    editing_mode = models.BooleanField(default=False)

    objects = FieldManager()

    def __str__(self):
        return self.field_name
