from django.db import models

# Create your models here.
class Process(models.Model):
    process_name = models.CharField(max_length=100, default="New Process Template")
    process_date_created = models.DateTimeField('process date created', auto_now_add=True)
    workcenter = models.CharField('work center', max_length=5)


    class Meta:
        verbose_name_plural = "processes"


    def __str__(self):
        return self.process_name


class OutlineField(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    OUTLINE_field_name = models.CharField(max_length=100)
    OUTLINE_field_text = models.CharField(max_length=200, blank=True)
    OUTLINE_name_is_operator_editable = models.BooleanField(default=True)
    OUTLINE_text_is_operator_editable = models.BooleanField(default=True)
    OUTLINE_required_for_full_submission = models.BooleanField(default=True)
    OUTLINE_can_be_deleted = models.BooleanField(default=True)

    def __str__(self):
        return self.OUTLINE_field_name
