import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Create your models here.
class Job(models.Model):
    job_id = models.CharField(max_length=20, default="New Job")
    date_created = models.DateTimeField('date created', auto_now_add=True)
    last_update = models.DateTimeField('last updated', default=timezone.now)
    process_outline = models.CharField(max_length=200, default="None")

    def __str__(self):
        return self.job_id

    def get_absolute_url(self):
        return reverse('embossers:detail', kwargs={'pk': self.pk})

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
    name_is_operator_editable = models.BooleanField(default=True)
    text_is_operator_editable = models.BooleanField(default=True)
    required_for_full_submission = models.BooleanField(default=True)

    objects = FieldManager()

    def __str__(self):
        return self.field_name
