from django.db import models

# Create your models here.
class WorkCenter(models.Model):
    workcenter_id = models.CharField(max_length=5, unique=True)

    class Meta:
        verbose_name_plural = "work centers"

    def __str__(self):
        return self.workcenter_id


class Worker(models.Model):
    timecard_id = models.DecimalField(db_column='lmpTimecardID', max_digits=9, decimal_places=0, primary_key=True)
    employee_id = models.CharField(db_column='lmpEmployeeID', max_length=10)
    start_time = models.DateTimeField(db_column='lmpActualStartTime', blank=True, null=True)
    end_time = models.DateTimeField(db_column='lmpActualEndTime', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Timecards'

    def __str__(self):
        return self.employee_id


class Operation(models.Model):
    timecard_id = models.DecimalField(db_column='lmlTimecardID', max_digits=9, decimal_places=0)
    timecard_line_id = models.DecimalField(db_column='lmlTimecardLineID', max_digits=4, decimal_places=0)
    job_id = models.CharField(db_column='lmlJobID', max_length=20)
    assembly_id = models.IntegerField(db_column='lmlJobAssemblyID')
    operation_id = models.IntegerField(db_column='lmlJobOperationID')
    work_center_id = models.CharField(db_column='lmlWorkCenterID', max_length=5)
    employee_id = models.CharField(db_column='lmlEmployeeID', max_length=10)
    uuid = models.CharField(db_column='lmlUniqueID', max_length=36, primary_key=True)
    start_time = models.DateTimeField(db_column='lmlActualStartTime')
    end_time = models.DateTimeField(db_column='lmlActualEndTime')
    active = models.IntegerField(db_column='lmlActive')

    class Meta:
        managed = False
        db_table = 'TimecardLines'
