from django.db import models

from embossers.models import Job as EmbosserJob
from processes.models import Process

# Create your models here.
class Job(models.Model):
    job_number = models.CharField(max_length=100)
    assembly_number = models.CharField(max_length=100)
    operation_number = models.CharField(max_length=100)
    job_type = models.CharField('job type', max_length=100, default="embosser")
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_due = models.DateTimeField('date due', blank=True, null=True)
    process_outline = models.CharField(max_length=100, default="None", verbose_name="Process Template")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return (self.job_number + "-" + self.assembly_number + "-" + self.operation_number)

class Field(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    field_text = models.CharField(max_length=200, blank=True)
    name_is_operator_editable = models.BooleanField(default=True)
    text_is_operator_editable = models.BooleanField(default=True)
    required_for_full_submission = models.BooleanField(default=True)
    is_associated_with_a_template = models.BooleanField(default=False)

    def __str__(self):
        return self.field_name
